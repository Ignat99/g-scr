BEGIN TRANSACTION;
CREATE TABLE tree_nodes (node_id integer primary key, parent integer, type text, name text, diagram_id integer);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (1,0,'item',NULL,1);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (2,0,'item',NULL,2);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (3,0,'folder','Quick sort',NULL);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (7,3,'folder','Sorter methods',NULL);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (9,7,'item','',7);
CREATE TABLE state (row integer primary key, current_dia integer, description text);
INSERT INTO `state` (row,current_dia,description) VALUES (1,7,'=== header ===
#!/usr/bin/env python
# coding: utf-8

import sys

# Символы Юникод

=== class ===
class Sorter:
    foo = ""

=== footer ===
main()');
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
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (4,1,'vertical','',0,500,420,0,340,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (5,1,'horizontal','',0,530,420,140,0,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (6,1,'action','x',0,690,420,50,20,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (7,2,'beginend','rmsnorm2',0,170,20,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (8,2,'beginend','Конец',0,170,350,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (9,2,'action','ms = sum((yi * yi for yi in y)) / len(y)
scale = (ms + 1e-05) ** (-0.5)
return [yi * scale for yi in y]',0,170,150,170,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (10,2,'vertical','',0,170,20,0,340,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (11,2,'horizontal','',0,200,20,140,0,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (12,2,'action','y',0,360,20,50,20,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (114,7,'beginend','__init__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (115,7,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (116,7,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (117,7,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (118,7,'action','#method
self
comparer',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (119,7,'action','self.comparer = comparer',0,170,170,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (120,7,'commentout','Note that the argument list starts with
#comment
This makes the current procedure 
to be added as a method to the class.',0,610,60,170,50,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (121,7,'commentin','In order to make the code generator create a class,
add something like this to the File description:

=== class ===
class Sorter

Only one class per file is supported.',0,570,260,228,70,60,0,NULL,'',NULL,'');
CREATE TABLE info (key text primary key, value text);
INSERT INTO `info` (key,value) VALUES ('type','drakon');
INSERT INTO `info` (key,value) VALUES ('version','33');
INSERT INTO `info` (key,value) VALUES ('start_version','1');
INSERT INTO `info` (key,value) VALUES ('language','Python 3.x');
CREATE TABLE diagrams (diagram_id integer primary key, name text unique, origin text, description text, zoom double);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (1,'rmsnorm','0 250',NULL,120.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (2,'rmsnorm2','-41 -82',NULL,120.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (7,'__init__','24 -13','The constructor of class Sorter.',100.0);
CREATE TABLE diagram_info (diagram_id integer, name text, value text, primary key (diagram_id, name));
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (1,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (1,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (2,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (2,'orientation','portrait');
COMMIT;
