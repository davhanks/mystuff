import ldap

Server = "ldap://172.18.31.2"
conn = ldap.initialize(Server)

conn.simple_bind_s("michael")