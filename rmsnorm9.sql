BEGIN TRANSACTION;
CREATE TABLE tree_nodes (node_id integer primary key, parent integer, type text, name text, diagram_id integer);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (1,0,'item',NULL,1);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (2,0,'item',NULL,2);
CREATE TABLE state (row integer primary key, current_dia integer, description text);
INSERT INTO `state` (row,current_dia,description) VALUES (1,2,NULL);
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
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (1,1,'beginend','rmsnorm',1,500,420,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (2,1,'beginend','Конец',1,500,750,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (3,1,'action','ms = sum((xi * xi for xi in x)) / len(x)
scale = (ms + 1e-05) ** (-0.5)
return [xi * scale for xi in x]',1,500,550,170,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (6,1,'vertical','',1,500,420,0,340,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (8,1,'horizontal','',1,530,420,140,0,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (9,1,'action','x',1,690,420,50,20,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (10,2,'beginend','rmsnorm2',0,170,20,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (11,2,'beginend','Конец',0,170,350,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (12,2,'action','ms = sum((yi * yi for yi in y)) / len(y)
scale = (ms + 1e-05) ** (-0.5)
return [yi * scale for yi in y]',0,170,150,170,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (13,2,'vertical','',0,170,20,0,340,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (14,2,'horizontal','',0,200,20,140,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (15,2,'action','y',0,360,20,50,20,0,0,NULL,'',NULL,'');
CREATE TABLE info (key text primary key, value text);
INSERT INTO `info` (key,value) VALUES ('type','drakon');
INSERT INTO `info` (key,value) VALUES ('version','33');
INSERT INTO `info` (key,value) VALUES ('start_version','1');
INSERT INTO `info` (key,value) VALUES ('language','Python 3.x');
CREATE TABLE diagrams (diagram_id integer primary key, name text unique, origin text, description text, zoom double);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (1,'rmsnorm','0 250',NULL,120.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (2,'rmsnorm2','-41 -82',NULL,120.0);
CREATE TABLE diagram_info (diagram_id integer, name text, value text, primary key (diagram_id, name));
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (1,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (1,'orientation','portrait');
COMMIT;
