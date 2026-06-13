-- ============================================================
-- SlimThuis — databaseschema voor Supabase
-- Plak dit hele script in: Supabase dashboard → SQL Editor → Run
-- ============================================================

-- Huishoudens: één rij per huishouden, met alle app-data als JSON
create table public.huishoudens (
  id uuid primary key default gen_random_uuid(),
  code text unique not null,
  data jsonb not null default '{}'::jsonb,
  bijgewerkt timestamptz not null default now()
);

-- Leden: wie hoort bij welk huishouden
create table public.leden (
  user_id uuid not null references auth.users(id) on delete cascade,
  huishouden_id uuid not null references public.huishoudens(id) on delete cascade,
  primary key (user_id, huishouden_id)
);

-- Row Level Security: iedereen kan alléén het eigen huishouden zien
alter table public.huishoudens enable row level security;
alter table public.leden enable row level security;

create policy "lid ziet eigen lidmaatschap"
  on public.leden for select using (auth.uid() = user_id);

create policy "lid verlaat zelf huishouden"
  on public.leden for delete using (auth.uid() = user_id);

create policy "leden lezen hun huishouden"
  on public.huishoudens for select using (
    exists (select 1 from public.leden
            where leden.huishouden_id = huishoudens.id
              and leden.user_id = auth.uid()));

create policy "leden werken hun huishouden bij"
  on public.huishoudens for update using (
    exists (select 1 from public.leden
            where leden.huishouden_id = huishoudens.id
              and leden.user_id = auth.uid()))
  with check (
    exists (select 1 from public.leden
            where leden.huishouden_id = huishoudens.id
              and leden.user_id = auth.uid()));

-- Huishouden starten (maakt rij + lidmaatschap, geeft deelcode terug)
create or replace function public.start_huishouden(begin_data jsonb)
returns table(id uuid, code text)
language plpgsql security definer set search_path = public
as $$
declare
  nieuwe_id uuid;
  nieuwe_code text;
begin
  nieuwe_code := upper(substr(md5(random()::text || clock_timestamp()::text), 1, 6));
  insert into huishoudens (code, data)
    values (nieuwe_code, coalesce(begin_data, '{}'::jsonb))
    returning huishoudens.id into nieuwe_id;
  insert into leden (user_id, huishouden_id) values (auth.uid(), nieuwe_id);
  return query select nieuwe_id, nieuwe_code;
end $$;

-- Aansluiten bij een bestaand huishouden met de deelcode
create or replace function public.sluit_aan(invitecode text)
returns uuid
language plpgsql security definer set search_path = public
as $$
declare hid uuid;
begin
  select huishoudens.id into hid
    from huishoudens
   where huishoudens.code = upper(trim(invitecode));
  if hid is null then
    raise exception 'Code niet gevonden';
  end if;
  insert into leden (user_id, huishouden_id)
    values (auth.uid(), hid)
    on conflict do nothing;
  return hid;
end $$;

revoke all on function public.start_huishouden(jsonb) from public;
revoke all on function public.sluit_aan(text) from public;
grant execute on function public.start_huishouden(jsonb) to authenticated;
grant execute on function public.sluit_aan(text) to authenticated;

-- Realtime aanzetten zodat wijzigingen direct op andere apparaten verschijnen
alter publication supabase_realtime add table public.huishoudens;
