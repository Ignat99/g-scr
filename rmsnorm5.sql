BEGIN TRANSACTION;
CREATE TABLE tree_nodes (node_id integer primary key, parent integer, type text, name text, diagram_id integer);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (1,0,'item',NULL,1);
CREATE TABLE state (row integer primary key, current_dia integer, description text);
INSERT INTO `state` (row,current_dia,description) VALUES (1,1,NULL);
CREATE TABLE items (
                item_id integer primary key,
                diagram_id integer,
                type text,
                text text,
                selected integer,
                x integer,
                y integer,
                w integer,
                h integer,
                a integer,
                b integer,
                aux_value integer,
                color text,
                format text,
                text2 text
            );
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (1,1,'beginend','rmsnorm',0,500,420,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (2,1,'beginend','Конец',0,500,750,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (3,1,'action','ms = sum((xi * xi for xi in x)) / len(x)
scale = (ms + 1e-05) ** (-0.5)
return [xi * scale for xi in x]',0,500,550,170,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (4,1,'vertical','',0,510,420,0,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (5,1,'vertical','',0,510,550,0,0,0,0,NULL,'',NULL,'');
CREATE TABLE info (key text primary key, value text);
INSERT INTO `info` (key,value) VALUES ('type','drakon');
INSERT INTO `info` (key,value) VALUES ('version','33');
INSERT INTO `info` (key,value) VALUES ('start_version','1');
INSERT INTO `info` (key,value) VALUES ('language','Python 3.x');
CREATE TABLE diagrams (diagram_id integer primary key, name text unique, origin text, description text, zoom double);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (1,'rmsnorm','208 291',NULL,120.0);
CREATE TABLE diagram_info (diagram_id integer, name text, value text, primary key (diagram_id, name));
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (1,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (1,'orientation','portrait');
COMMIT;
