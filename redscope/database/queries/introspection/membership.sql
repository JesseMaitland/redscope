SELECT usename AS user_name,
       groname AS group_name
  FROM pg_user u
       INNER JOIN pg_group g
          ON u.usesysid = ANY(g.grolist)
ORDER BY user_name, group_name;
