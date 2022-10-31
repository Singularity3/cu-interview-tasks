select distinct dp.dir_uid as username
  ,de.mail as email
  ,case  
	when dp.primaryaffiliation in ('Staff', 'Officer/Professional') then 'Faculty/Staff'
    when dp.primaryaffiliation = 'Faculty' and not (daf.edupersonaffiliation = 'Faculty' and daf.description = 'Student Faculty') then 'Faculty/Staff'
    when dp.primaryaffiliation = 'Employee' and not (daf.edupersonaffiliation = 'Employee'
        and daf.description in ('Student Employee', 'Student Faculty')) then 'Faculty/Staff'
    when dp.primaryaffiliation = 'Member'
      and daf.edupersonaffiliation = 'Member'
      and daf.description = 'Faculty' then 'Faculty/Staff'
    else 'Student'
  end as person_type
from dirsvcs.dir_person dp 
  inner join dirsvcs.dir_affiliation daf
    on daf.uuid = dp.uuid
    and daf.campus = 'Boulder Campus' 
    and dp.primaryaffiliation not in ('Not currently affiliated', 'Retiree', 'Affiliate', 'Member')
    and daf.description not in ('Admitted Student', 'Alum', 'Confirmed Student', 'Former Student', 'Member Spouse', 'Sponsored', 'Sponsored EFL', 'Retiree', 'Boulder3')
    and daf.description not like 'POI_%'
  inner join dirsvcs.dir_email de
    on de.uuid = dp.uuid
    and de.mail_flag = 'M'
    and de.mail is not null
	and lower(de.mail) not like '%cu.edu'
where dp.primaryaffiliation != 'Student'
  or exists (select 'x' from dirsvcs.dir_acad_career where uuid = dp.uuid)
