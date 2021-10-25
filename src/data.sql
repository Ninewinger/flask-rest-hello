
/* SELECCIONAR TODO(ctrl+a) Y EJECUTAR */

/* Create Active User */
insert into users(id,email,password,is_active) values('1','test@gmail.com','1234','1');

/* Insert Planets */
insert into planets(id,name,rotation_period,orbital_period,diameter,climate,gravity,terrain,surface_water,population) values('1','Tatooine','23','304','10465','arid','1 standard','desert','1','200000');
insert into planets(id,name,rotation_period,orbital_period,diameter,climate,gravity,terrain,surface_water,population) values('2','Alderaan','24','364','12500','temperate','1 standard','grasslands, mountains','40','2000000000');
insert into planets(id,name,rotation_period,orbital_period,diameter,climate,gravity,terrain,surface_water,population) values('3','Yavin IV','24','4818','10200','temperate, tropical','1 standard','jungle, rainforests','8','1000');
insert into planets(id,name,rotation_period,orbital_period,diameter,climate,gravity,terrain,surface_water,population) values('8','Naboo','26','312','12120','temperate','1 standard','grassy hills, swamps, forests, mountains','12','4500000000');

/* Insert Starships */
insert into starships(id,name,model,manufacturer,cost_in_credits,length,max_atmosphering_speed,crew,passengers,cargo_capacity,consumables,hyperdrive_rating,MGLT,starship_class) values('12','X-wing','T-65 X-wing','Incom Corporation','149999','12.5','1050','1','0','110','1 week','1','100','Starfighter');
insert into starships(id,name,model,manufacturer,cost_in_credits,length,max_atmosphering_speed,crew,passengers,cargo_capacity,consumables,hyperdrive_rating,MGLT,starship_class) values('22','Imperial shuttle','Lambda-class T-4a shuttle','Sienar Fleet Systems','240000','20','850','6','20','80000','2 months','1','50','Armed government transport');

/* Insert Characters */
insert into characters(id,name,height,mass,hair_color,skin_color,eye_color,birth_year,gender,homeworld_id) values('1','Luke Skywalker','172','77','blond','fair','blue','19BBY','male','1');
insert into characters(id,name,height,mass,hair_color,skin_color,eye_color,birth_year,gender,homeworld_id) values('2','C-3PO','167','75','n/a','gold','yellow','112BBY','n/a','1');
insert into characters(id,name,height,mass,hair_color,skin_color,eye_color,birth_year,gender,homeworld_id) values('3','R2-D2','96','32','n/a','white, blue','red','33BBY','n/a','8');

/* Bridge table starships-characters */
insert into ships(starship_id,character_id) values('12','1');
insert into ships(starship_id,character_id) values('22','1');

/* Bridge table fav-user */
insert into fav_characters(user_id,char_id) values('1','1');
insert into fav_characters(user_id,char_id) values('1','3');

/* Bridge table fav-planets */
insert into fav_planets(user_id,planet_id) values('1','1');