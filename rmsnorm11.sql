BEGIN TRANSACTION;
CREATE TABLE tree_nodes (node_id integer primary key, parent integer, type text, name text, diagram_id integer);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (3,0,'folder','Quick sort',NULL);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (7,3,'folder','Sorter methods',NULL);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (9,7,'item','',7);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (11,0,'item',NULL,1);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (12,0,'item',NULL,2);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (13,7,'item','',8);
CREATE TABLE state (row integer primary key, current_dia integer, description text);
INSERT INTO `state` (row,current_dia,description) VALUES (1,8,'=== header ===
#!/usr/bin/env python
# coding: utf-8

import sys

# Символы Юникод

=== class ===
class Sorter:
    foo = ''''

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
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (122,8,'beginend','quick_sort',0,110,60,50,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (123,8,'beginend','End',0,2220,510,50,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (124,8,'vertical','',0,110,80,0,710,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (125,8,'vertical','',0,780,120,0,670,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (126,8,'vertical','',0,2220,120,0,380,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (127,8,'horizontal','',0,110,120,2110,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (128,8,'arrow','',0,-20,120,130,670,1930,1,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (129,8,'branch','analyze input',0,110,170,110,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (130,8,'address','exit',0,110,750,110,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (131,8,'branch','simple case',0,780,170,150,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (132,8,'branch','partition',0,1450,170,160,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (133,8,'address','exit',0,780,750,150,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (134,8,'horizontal','',0,150,60,120,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (135,8,'action','#method

self
collection',0,310,60,50,50,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (136,8,'action','length = len(collection)',0,110,270,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (137,8,'select','length',0,110,380,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (138,8,'case','0',0,110,460,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (139,8,'case','1',0,280,460,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (140,8,'case','2',0,400,460,60,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (141,8,'branch','exit',0,2220,170,70,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (142,8,'horizontal','',0,110,420,410,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (143,8,'case','',0,520,460,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (144,8,'vertical','',0,280,420,0,80,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (145,8,'vertical','',0,520,420,0,370,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (146,8,'vertical','',0,400,420,0,370,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (147,8,'horizontal','',0,110,500,170,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (148,8,'action','result = collection',0,110,610,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (149,8,'address','simple case',0,400,750,60,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (150,8,'vertical','',0,1450,120,0,670,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (151,8,'address','recurse',0,1450,750,160,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (152,8,'address','partition',0,520,750,50,30,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (153,8,'action','first = collection[0]
second = collection[1]',0,780,290,150,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (154,8,'if','self.comparer(first, second) < 0',0,780,360,150,20,140,1,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (155,8,'action','result = [ second, first ]',0,1070,610,120,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (156,8,'vertical','',0,1070,360,0,300,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (157,8,'horizontal','',0,780,660,290,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (158,8,'action','half = int(length / 2)
median = collection[half]
left = []
right = []',0,1450,270,160,50,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (159,8,'loopstart','i = 0; i < length; i += 1',0,1450,360,160,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (160,8,'loopend','',0,1450,690,160,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (161,8,'action','current = collection[i]',0,1450,480,160,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (162,8,'if','self.comparer(current, median) < 0',0,1450,540,160,20,120,1,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (163,8,'action','left.append(current)',0,1450,610,160,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (164,8,'action','right.append(current)',0,1730,610,100,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (165,8,'horizontal','',0,1450,650,390,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (166,8,'vertical','',0,1730,540,0,110,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (167,8,'branch','recurse',0,1910,170,160,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (168,8,'address','exit',0,1910,750,160,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (169,8,'vertical','',0,1910,120,0,670,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (170,8,'action','left_sorted = self.quick_sort(left)
right_sorted = self.quick_sort(right)',0,1910,250,160,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (171,8,'action','result = []
result.extend(left_sorted)
result.append(median)
result.extend(right_sorted)',0,1910,340,160,50,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (172,8,'if','i == half',0,1450,410,160,20,230,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (173,8,'vertical','',0,1840,410,0,240,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (174,8,'action','result = collection',0,780,610,150,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (175,8,'action','return result',0,2220,420,70,20,0,0,NULL,'',NULL,'');
CREATE TABLE info (key text primary key, value text);
INSERT INTO `info` (key,value) VALUES ('type','drakon');
INSERT INTO `info` (key,value) VALUES ('version','33');
INSERT INTO `info` (key,value) VALUES ('start_version','1');
INSERT INTO `info` (key,value) VALUES ('language','Python 3.x');
CREATE TABLE diagrams (diagram_id integer primary key, name text unique, origin text, description text, zoom double);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (1,'rmsnorm','0 250',NULL,120.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (2,'rmsnorm2','-41 -82',NULL,120.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (7,'__init__','24 -13','The constructor of class Sorter.',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (8,'quick_sort','-40 14','The classic quick sort algorithm.

Implemented as a method in a class.
The comparison function is stored
in the field ''comparer''.',100.0);
CREATE TABLE diagram_info (diagram_id integer, name text, value text, primary key (diagram_id, name));
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (1,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (1,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (2,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (2,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (7,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (7,'orientation','portrait');
COMMIT;
