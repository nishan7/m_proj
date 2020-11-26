BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "mapp_orderitem" (
	"id"	INTEGER,
	"title_id"	integer,
	FOREIGN KEY("title_id") REFERENCES "mapp_item"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "mapp_item" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"title"	varchar(100) NOT NULL,
	"price"	real NOT NULL,
	"category"	varchar(2) NOT NULL,
	"label"	varchar(1) NOT NULL,
	"slug"	varchar(50) NOT NULL,
	"description"	text NOT NULL,
	"discount_price"	real,
	"image"	varchar(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS "mapp_order_items" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"order_id"	integer NOT NULL,
	"orderitem_id"	integer NOT NULL,
	FOREIGN KEY("order_id") REFERENCES "mapp_order"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("orderitem_id") REFERENCES "mapp_orderitem"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "mapp_order" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"ref_code"	varchar(20),
	"start_date"	datetime NOT NULL,
	"ordered_date"	datetime NOT NULL,
	"ordered"	bool NOT NULL
);
CREATE TABLE IF NOT EXISTS "accounts_customuser" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"email"	varchar(254) NOT NULL UNIQUE,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"mobile_number"	varchar(128) NOT NULL,
	"seller"	bool NOT NULL,
	"name"	varchar(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "products_product" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"name"	varchar(100) NOT NULL,
	"slug"	varchar(50) NOT NULL,
	"preview_text"	text NOT NULL,
	"detail_text"	text NOT NULL,
	"price"	real NOT NULL,
	"category_id"	varchar(100) NOT NULL,
	"mainimage"	varchar(100) NOT NULL,
	FOREIGN KEY("category_id") REFERENCES "products_category"("title") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "products_category" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"primary_Category"	bool NOT NULL,
	"title"	varchar(100) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
CREATE TABLE IF NOT EXISTS "cart_order_orderitems" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"order_id"	integer NOT NULL,
	"cart_id"	integer NOT NULL,
	FOREIGN KEY("order_id") REFERENCES "cart_order"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("cart_id") REFERENCES "cart_cart"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "cart_order" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"ordered"	bool NOT NULL,
	"created"	datetime NOT NULL,
	"paymentId"	varchar(200),
	"orderId"	varchar(200),
	"user_id"	integer NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "accounts_customuser"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "cart_cart" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"quantity"	integer NOT NULL,
	"purchased"	bool NOT NULL,
	"created"	datetime NOT NULL,
	"item_id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "accounts_customuser"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("item_id") REFERENCES "products_product"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"action_time"	datetime NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	integer NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag">=0),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "accounts_customuser"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "accounts_customuser_user_permissions" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"customuser_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("customuser_id") REFERENCES "accounts_customuser"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "accounts_customuser_groups" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"customuser_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("customuser_id") REFERENCES "accounts_customuser"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"name"	varchar(150) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL
);
INSERT INTO "mapp_item" ("id","title","price","category","label","slug","description","discount_price","image") VALUES (2,'product3',20.0,'SW','D','product_fiel3','default description',NULL,'dsfs.jpg'),
 (3,'product2',33.0,'S','S','product_field2','default description',NULL,'ab_68X2N0A.png');
INSERT INTO "accounts_customuser" ("id","password","last_login","is_superuser","email","is_staff","is_active","date_joined","mobile_number","seller","name") VALUES (1,'bcrypt_sha256$$2b$12$Q4.HdjsXn6oYPAZ0roG8s.qOVOYW6iOUgIBcduw0Gfd1Bl0chqGTy',NULL,0,'nishan.paudel1914@gmail.com',0,1,'2020-01-18 17:45:41.986866','+919035468097',0,'Nishan Paudel'),
 (2,'bcrypt_sha256$$2b$12$hLevo/uy4NKQhvIH4s.f0ee1GFo93LPwbzt5GoylD2VDUOWIbFZwG','2020-01-19 05:49:05.024284',0,'kal@kjlfds.clkas',0,1,'2020-01-18 17:47:24.585230','',0,'kal Drogo'),
 (3,'bcrypt_sha256$$2b$12$/3c2Gi2hZwjKRkrYyrGpaOQ19PQdX5iOEwl0fAfNZQG6g/AexonDu',NULL,0,'sadf@gksl.com',0,1,'2020-01-19 04:40:43.410238','+919035468099',1,'Von hander'),
 (4,'bcrypt_sha256$$2b$12$EpjQGO/L2BCuuyzqJgquGOWiZqpk3DufXNaSfl6ArJG45CMDjSFsW','2020-01-21 18:37:18.816480',1,'ni@gmail.com',1,1,'2020-01-19 06:14:14.205321','',0,'Pepe');
INSERT INTO "products_product" ("id","name","slug","preview_text","detail_text","price","category_id","mainimage") VALUES (1,'Cole-Schneider','cole-schneider','account','Cell growth tonight. Step course choose smile clearly.',2.0,'tshirt','lan.png'),
 (2,'Herman-Rodriguez','herman-rodriguez','measure','Right exactly kitchen themselves daughter. Run conference care treatment.',6.0,'tshirt',''),
 (3,'Harris-James','harris-james','probably','Pick positive management project. Front pressure place chair southern.',1.0,'tshirt',''),
 (4,'Glover Ltd','glover-ltd','seek','Person order million. Key during car meet.',3.0,'tshirt',''),
 (5,'Ellis Group','ellis-group','forget','Different training board hope first experience yard. Common staff sometimes once.',2.0,'tshirt',''),
 (6,'Schneider Ltd','schneider-ltd','no','Cultural former go example girl help. Write late play heart himself result.',9.0,'tshirt',''),
 (7,'Ferrell, James and Moore','ferrell-james-and-moore','community','Foreign house discover school work management include. Spend Mr whose.',5.0,'tshirt',''),
 (8,'Jensen-Dominguez','jensen-dominguez','pull','Key soon strong close. Note tonight air situation common bill. Upon still imagine bill start onto.',4.0,'tshirt',''),
 (9,'Berry, Clark and Klein','berry-clark-and-klein','of','Natural these century body general particularly. Anything idea trouble yard nearly law.',9.0,'tshirt',''),
 (10,'Li, Vega and Lewis','li-vega-and-lewis','draw','No detail this us heavy right traditional. Ten other ahead here.
That purpose natural minute.',8.0,'tshirt',''),
 (11,'sdfds tshirt','sdfds-tshirt','preview','detail',200.0,'tshirt',''),
 (12,'Cool id card2','cool-id-card2','id card preview 3','id card details',200.0,'tshirt',''),
 (13,'Cool id card2','cool-id-card2','id card preview 3','id card details',200.0,'tshirt',''),
 (14,'Cool id card2','cool-id-card2','id card preview 3','id card details',200.0,'tshirt',''),
 (15,'lan','lan','lan preview','lan detail',200.0,'Pants','product'),
 (16,'house of cards','house-of-cards','house of cards preview','house of cards details',400.0,'tshirt',''),
 (17,'house of cards','house-of-cards','house of cards preview','house of cards details',400.0,'tshirt',''),
 (18,'sadf','sadf','sfda','sdf',23.0,'tshirt','products/dsfs.jpg'),
 (19,'213423','213423','ewewqr','eweqw',23443.0,'tshirt','products/lan.png'),
 (20,'Nishan Paudel','nishan-paudel','fsd','sdfs',23423.0,'tshirt','products/House_of_Cards_US__S01E05.mkv_snapshot_06.00.911.jpg'),
 (21,'Cool id card2','cool-id-card2','23243214','2413234',13214.0,'tshirt','products/Screenshot_1.png'),
 (22,'rwre','rwre','weqrr','qwre',324234.0,'tshirt','products/Screenshot_1_uhWXxgu.png'),
 (23,'1234','1234','weqrr','qwre',324234.0,'tshirt','products/Screenshot_11.png'),
 (24,'2344124','2344124','4321','1234',234243.0,'tshirt','products/Screenshot_25.png'),
 (25,'sdaf','sdaf','fsdaf','dsfafsd',123.0,'tshirt','products/Screenshot_56.png');
INSERT INTO "products_category" ("id","primary_Category","title") VALUES (1,1,'tshirt'),
 (2,0,'Pants');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('uzype8jmcbvnslyy3dnfbbx9k4st1051','YjQxNjkyYTZiNjI3OGIxZDZlY2M5NDI1ZjE5MzFmNTg1MWViZDY4MDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNGY1ODhjNTQyNGNjZTdmZjNiNjM5ZGQxNjI3OWE1ZTA5MjcwNDJlIn0=','2020-02-02 06:14:32.317540'),
 ('3qeddxsg1r7kpu7v9jt0puhseis1w7jr','YjQxNjkyYTZiNjI3OGIxZDZlY2M5NDI1ZjE5MzFmNTg1MWViZDY4MDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNGY1ODhjNTQyNGNjZTdmZjNiNjM5ZGQxNjI3OWE1ZTA5MjcwNDJlIn0=','2020-02-04 18:04:39.811312'),
 ('umiekldz6amjf8pvrd7ypfw89detdua4','YjQxNjkyYTZiNjI3OGIxZDZlY2M5NDI1ZjE5MzFmNTg1MWViZDY4MDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNGY1ODhjNTQyNGNjZTdmZjNiNjM5ZGQxNjI3OWE1ZTA5MjcwNDJlIn0=','2020-02-04 18:37:18.827373');
INSERT INTO "django_admin_log" ("id","action_time","object_id","object_repr","change_message","content_type_id","user_id","action_flag") VALUES (1,'2020-01-19 06:14:52.661218','0','','',5,4,3),
 (2,'2020-01-19 06:15:12.176131','2','Pants','[{"added": {}}]',5,4,1),
 (3,'2020-01-19 06:16:55.482097','15','lan','[{"added": {}}]',6,4,1),
 (4,'2020-01-21 18:05:12.139139','3','product2','[{"changed": {"fields": ["title", "label", "slug"]}}]',12,4,2),
 (5,'2020-01-21 18:05:41.066241','2','product3','[{"changed": {"fields": ["title", "label", "slug"]}}]',12,4,2),
 (6,'2020-01-21 18:11:50.284036','2','product3','[{"changed": {"fields": ["slug"]}}]',12,4,2),
 (7,'2020-01-21 18:12:07.475236','2','product3','[{"changed": {"fields": ["category"]}}]',12,4,2),
 (8,'2020-01-21 18:12:12.588358','2','product3','[{"changed": {"fields": ["label"]}}]',12,4,2),
 (9,'2020-01-21 18:23:00.514541','2','product3','[{"changed": {"fields": ["image"]}}]',12,4,2),
 (10,'2020-01-21 18:25:01.084781','2','product3','[{"changed": {"fields": ["image"]}}]',12,4,2),
 (11,'2020-01-21 18:28:03.460963','3','product2','[{"changed": {"fields": ["image"]}}]',12,4,2),
 (12,'2020-01-21 18:37:34.735354','3','product2','[{"changed": {"fields": ["image"]}}]',12,4,2),
 (13,'2020-01-21 18:48:39.948979','3','product2','[{"changed": {"fields": ["image"]}}]',12,4,2),
 (14,'2020-01-21 18:55:55.251477','2','product3','[{"changed": {"fields": ["image"]}}]',12,4,2);
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (1,1,'add_students','Can add students'),
 (2,1,'change_students','Can change students'),
 (3,1,'delete_students','Can delete students'),
 (4,1,'view_students','Can view students'),
 (5,2,'add_cart','Can add cart'),
 (6,2,'change_cart','Can change cart'),
 (7,2,'delete_cart','Can delete cart'),
 (8,2,'view_cart','Can view cart'),
 (9,3,'add_order','Can add order'),
 (10,3,'change_order','Can change order'),
 (11,3,'delete_order','Can delete order'),
 (12,3,'view_order','Can view order'),
 (13,4,'add_customuser','Can add custom user'),
 (14,4,'change_customuser','Can change custom user'),
 (15,4,'delete_customuser','Can delete custom user'),
 (16,4,'view_customuser','Can view custom user'),
 (17,5,'add_category','Can add category'),
 (18,5,'change_category','Can change category'),
 (19,5,'delete_category','Can delete category'),
 (20,5,'view_category','Can view category'),
 (21,6,'add_product','Can add product'),
 (22,6,'change_product','Can change product'),
 (23,6,'delete_product','Can delete product'),
 (24,6,'view_product','Can view product'),
 (25,7,'add_logentry','Can add log entry'),
 (26,7,'change_logentry','Can change log entry'),
 (27,7,'delete_logentry','Can delete log entry'),
 (28,7,'view_logentry','Can view log entry'),
 (29,8,'add_permission','Can add permission'),
 (30,8,'change_permission','Can change permission'),
 (31,8,'delete_permission','Can delete permission'),
 (32,8,'view_permission','Can view permission'),
 (33,9,'add_group','Can add group'),
 (34,9,'change_group','Can change group'),
 (35,9,'delete_group','Can delete group'),
 (36,9,'view_group','Can view group'),
 (37,10,'add_contenttype','Can add content type'),
 (38,10,'change_contenttype','Can change content type'),
 (39,10,'delete_contenttype','Can delete content type'),
 (40,10,'view_contenttype','Can view content type'),
 (41,11,'add_session','Can add session'),
 (42,11,'change_session','Can change session'),
 (43,11,'delete_session','Can delete session'),
 (44,11,'view_session','Can view session'),
 (45,12,'add_item','Can add item'),
 (46,12,'change_item','Can change item'),
 (47,12,'delete_item','Can delete item'),
 (48,12,'view_item','Can view item'),
 (49,13,'add_orderitem','Can add order item'),
 (50,13,'change_orderitem','Can change order item'),
 (51,13,'delete_orderitem','Can delete order item'),
 (52,13,'view_orderitem','Can view order item'),
 (53,14,'add_order','Can add order'),
 (54,14,'change_order','Can change order'),
 (55,14,'delete_order','Can delete order'),
 (56,14,'view_order','Can view order');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (1,'mapp','students'),
 (2,'cart','cart'),
 (3,'cart','order'),
 (4,'accounts','customuser'),
 (5,'products','category'),
 (6,'products','product'),
 (7,'admin','logentry'),
 (8,'auth','permission'),
 (9,'auth','group'),
 (10,'contenttypes','contenttype'),
 (11,'sessions','session'),
 (12,'mapp','item'),
 (13,'mapp','orderitem'),
 (14,'mapp','order');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (1,'contenttypes','0001_initial','2020-01-18 17:30:53.732474'),
 (2,'contenttypes','0002_remove_content_type_name','2020-01-18 17:30:53.761947'),
 (3,'auth','0001_initial','2020-01-18 17:30:53.811628'),
 (4,'auth','0002_alter_permission_name_max_length','2020-01-18 17:30:53.844293'),
 (5,'auth','0003_alter_user_email_max_length','2020-01-18 17:30:53.876896'),
 (6,'auth','0004_alter_user_username_opts','2020-01-18 17:30:53.901601'),
 (7,'auth','0005_alter_user_last_login_null','2020-01-18 17:30:53.932391'),
 (8,'auth','0006_require_contenttypes_0002','2020-01-18 17:30:53.952461'),
 (9,'auth','0007_alter_validators_add_error_messages','2020-01-18 17:30:53.981456'),
 (10,'auth','0008_alter_user_username_max_length','2020-01-18 17:30:54.011733'),
 (11,'auth','0009_alter_user_last_name_max_length','2020-01-18 17:30:54.048098'),
 (12,'auth','0010_alter_group_name_max_length','2020-01-18 17:30:54.086046'),
 (13,'auth','0011_update_proxy_permissions','2020-01-18 17:30:54.112732'),
 (14,'accounts','0001_initial','2020-01-18 17:30:54.154345'),
 (15,'admin','0001_initial','2020-01-18 17:30:54.196316'),
 (16,'admin','0002_logentry_remove_auto_add','2020-01-18 17:30:54.242260'),
 (17,'admin','0003_logentry_add_action_flag_choices','2020-01-18 17:30:54.291034'),
 (18,'products','0001_initial','2020-01-18 17:30:54.339390'),
 (19,'cart','0001_initial','2020-01-18 17:30:54.436668'),
 (21,'sessions','0001_initial','2020-01-18 17:30:54.474725'),
 (22,'accounts','0002_auto_20200118_2359','2020-01-18 18:29:45.036431'),
 (23,'products','0002_auto_20200119_1024','2020-01-19 04:54:51.963333'),
 (24,'products','0003_auto_20200119_1027','2020-01-19 04:57:17.335657'),
 (25,'products','0004_auto_20200119_1028','2020-01-19 04:58:45.526964'),
 (26,'products','0005_auto_20200119_1038','2020-01-19 05:10:35.967928'),
 (27,'products','0006_auto_20200119_1053','2020-01-19 05:23:11.943260'),
 (28,'products','0007_auto_20200119_1107','2020-01-19 05:37:23.053704'),
 (29,'products','0008_auto_20200119_1126','2020-01-19 05:56:51.387613'),
 (30,'accounts','0003_auto_20200119_1143','2020-01-19 06:13:41.492166'),
 (31,'products','0009_auto_20200119_1143','2020-01-19 06:13:41.507166'),
 (32,'products','0010_auto_20200119_1241','2020-01-19 07:11:45.818517'),
 (33,'products','0011_auto_20200119_1246','2020-01-19 07:16:05.401101'),
 (34,'accounts','0002_customuser_name','2020-01-19 10:21:08.232840'),
 (35,'accounts','0003_auto_20200119_1552','2020-01-19 10:22:08.396580'),
 (37,'mapp','0002_auto_20200121_2222','2020-01-21 16:52:31.670695'),
 (38,'mapp','0003_item_slug','2020-01-21 17:21:50.178632'),
 (39,'mapp','0004_auto_20200121_2338','2020-01-21 18:08:29.313596'),
 (40,'mapp','0005_auto_20200121_2352','2020-01-21 18:22:13.794831'),
 (41,'mapp','0006_auto_20200121_2354','2020-01-21 18:24:52.203393'),
 (42,'mapp','0007_auto_20200122_0026','2020-01-21 18:56:17.635229'),
 (43,'mapp','0001_initial','2020-01-22 13:02:45.393050');
CREATE INDEX IF NOT EXISTS "mapp_orderitem_title_id_8f9b469e" ON "mapp_orderitem" (
	"title_id"
);
CREATE INDEX IF NOT EXISTS "mapp_item_slug_583047b4" ON "mapp_item" (
	"slug"
);
CREATE INDEX IF NOT EXISTS "mapp_order_items_orderitem_id_8e420081" ON "mapp_order_items" (
	"orderitem_id"
);
CREATE INDEX IF NOT EXISTS "mapp_order_items_order_id_919e5be5" ON "mapp_order_items" (
	"order_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "mapp_order_items_order_id_orderitem_id_493bd039_uniq" ON "mapp_order_items" (
	"order_id",
	"orderitem_id"
);
CREATE INDEX IF NOT EXISTS "products_product_category_id_9b594869" ON "products_product" (
	"category_id"
);
CREATE INDEX IF NOT EXISTS "products_product_slug_70d3148d" ON "products_product" (
	"slug"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
CREATE INDEX IF NOT EXISTS "cart_order_orderitems_cart_id_6ad10cf1" ON "cart_order_orderitems" (
	"cart_id"
);
CREATE INDEX IF NOT EXISTS "cart_order_orderitems_order_id_c8c953d6" ON "cart_order_orderitems" (
	"order_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "cart_order_orderitems_order_id_cart_id_bc5ed76c_uniq" ON "cart_order_orderitems" (
	"order_id",
	"cart_id"
);
CREATE INDEX IF NOT EXISTS "cart_order_user_id_279b5d53" ON "cart_order" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "cart_cart_user_id_9b4220b9" ON "cart_cart" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "cart_cart_item_id_c66662e3" ON "cart_cart" (
	"item_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "accounts_customuser_user_permissions_permission_id_aea3d0e5" ON "accounts_customuser_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "accounts_customuser_user_permissions_customuser_id_0deaefae" ON "accounts_customuser_user_permissions" (
	"customuser_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "accounts_customuser_user_permissions_customuser_id_permission_id_9632a709_uniq" ON "accounts_customuser_user_permissions" (
	"customuser_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "accounts_customuser_groups_group_id_86ba5f9e" ON "accounts_customuser_groups" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "accounts_customuser_groups_customuser_id_bc55088e" ON "accounts_customuser_groups" (
	"customuser_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "accounts_customuser_groups_customuser_id_group_id_c074bdcb_uniq" ON "accounts_customuser_groups" (
	"customuser_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
COMMIT;
