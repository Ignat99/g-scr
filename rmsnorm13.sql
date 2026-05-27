BEGIN TRANSACTION;
CREATE TABLE tree_nodes (node_id integer primary key, parent integer, type text, name text, diagram_id integer);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (1,0,'folder','microgpt',NULL);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (2,1,'folder','Value',NULL);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (3,2,'item','__add__',1);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (4,2,'item','__init__',2);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (5,2,'item','__mul__',3);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (6,2,'item','__neg__',4);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (7,2,'item','__pow__',5);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (8,2,'item','__radd__',6);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (9,2,'item','__rmul__',7);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (10,2,'item','__rsub__',8);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (11,2,'item','__rtruediv__',9);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (12,2,'item','__sub__',10);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (13,2,'item','__truediv__',11);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (14,2,'item','backward',12);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (15,2,'item','exp',13);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (16,2,'item','log',14);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (17,2,'item','relu',15);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (18,1,'item','gpt',16);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (19,1,'item','linear',17);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (20,1,'item','main',18);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (21,1,'item','rmsnorm',19);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (22,1,'item','softmax',20);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (23,0,'item',NULL,21);
CREATE TABLE state (row integer primary key, current_dia integer, description text);
INSERT INTO `state` (row,current_dia,description) VALUES (1,21,'=== header ===
#!/usr/bin/env python
# coding: utf-8
# Символы Юникод

=== class ===
class Value:
    __slots__ = (''data'', ''grad'', ''_children'', ''_local_grads'')

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
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (1,1,'beginend','__add__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (2,1,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (3,1,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (4,1,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (5,1,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (6,1,'action','if isinstance(other, Value):
    other = other
else:
    other = Value(other)
return Value(self.data + other.data, (self, other), (1, 1))',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (11,2,'beginend','__init__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (12,2,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (13,2,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (14,2,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (15,2,'action','#method
self
data
children
local_grads',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (16,2,'action','self.data = data
self.grad = 0
self._children = children
self._local_grads = local_grads',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (21,3,'beginend','__mul__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (22,3,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (23,3,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (24,3,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (25,3,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (26,3,'action','if isinstance(other, Value):
    other = other
else:
    other = Value(other)
return Value(self.data * other.data, (self, other), (other.data, self.data))',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (31,4,'beginend','__neg__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (32,4,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (33,4,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (34,4,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (35,4,'action','#method
self',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (36,4,'action','return self * -1',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (41,5,'beginend','__pow__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (42,5,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (43,5,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (44,5,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (45,5,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (46,5,'action','return Value(self.data ** other, (self,), (other * self.data ** (other - 1),))',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (51,6,'beginend','__radd__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (52,6,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (53,6,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (54,6,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (55,6,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (56,6,'action','return self + other',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (61,7,'beginend','__rmul__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (62,7,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (63,7,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (64,7,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (65,7,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (66,7,'action','return self * other',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (71,8,'beginend','__rsub__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (72,8,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (73,8,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (74,8,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (75,8,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (76,8,'action','return other + -self',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (81,9,'beginend','__rtruediv__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (82,9,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (83,9,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (84,9,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (85,9,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (86,9,'action','return other * self ** (-1)',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (91,10,'beginend','__sub__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (92,10,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (93,10,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (94,10,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (95,10,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (96,10,'action','return self + -other',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (101,11,'beginend','__truediv__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (102,11,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (103,11,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (104,11,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (105,11,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (106,11,'action','return self * other ** (-1)',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (111,12,'beginend','backward',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (112,12,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (113,12,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (114,12,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (115,12,'action','#method
self',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (116,12,'action','topo = []
visited = set()
def build_topo(v):
    if v not in visited:
        visited.add(v)
        for child in v._children:
            build_topo(child)
        topo.append(v)
build_topo(self)
self.grad = 1
for v in reversed(topo):
    for child, local_grad in zip(v._children, v._local_grads):
        child.grad += local_grad * v.grad',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (121,13,'beginend','exp',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (122,13,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (123,13,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (124,13,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (125,13,'action','#method
self',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (126,13,'action','return Value(math.exp(self.data), (self,), (math.exp(self.data),))',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (131,14,'beginend','log',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (132,14,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (133,14,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (134,14,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (135,14,'action','#method
self',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (136,14,'action','return Value(math.log(self.data), (self,), (1 / self.data,))',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (141,15,'beginend','relu',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (142,15,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (143,15,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (144,15,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (145,15,'action','#method
self',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (146,15,'action','return Value(max(0, self.data), (self,), (float(self.data > 0),))',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (151,16,'beginend','gpt',0,150,60,60,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (152,16,'beginend','Конец',0,850,370,50,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (153,16,'horizontal','',0,150,120,700,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (154,16,'horizontal','',0,150,520,700,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (155,16,'vertical','',0,850,120,0,250,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (156,16,'horizontal','',0,190,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (157,16,'action','token_id
pos_id
keys
values',0,310,60,80,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (158,16,'vertical','',0,150,120,0,400,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (159,16,'branch','Q',0,150,160,140,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (160,16,'action','global n_layer
global n_head
global head_dim
tok_emb = state_dict[''wte''][token_id]
pos_emb = state_dict[''wpe''][pos_id]
x = [t + p for t, p in zip(tok_emb, pos_emb)]
x = rmsnorm(x)
logits = linear(x, state_dict[''lm_head''])
return logits',0,150,280,180,80,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (161,16,'address','E_T',0,150,420,140,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (162,16,'vertical','',0,500,120,0,400,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (163,16,'branch','E_T',0,500,160,140,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (164,16,'action','FOR li in range(n_layer)
CALL W',0,500,280,180,80,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (165,16,'address','Конец',0,500,420,140,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (511,17,'beginend','linear',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (512,17,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (513,17,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (514,17,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (515,17,'action','x
w',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (516,17,'action','return [sum((wi * xi for wi, xi in zip(wo, x))) for wo in w]',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (521,18,'beginend','main',0,150,60,60,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (522,18,'beginend','Конец',0,1550,370,50,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (523,18,'horizontal','',0,150,120,1400,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (524,18,'horizontal','',0,150,520,1400,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (525,18,'vertical','',0,1550,120,0,250,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (526,18,'vertical','',0,150,120,0,400,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (527,18,'branch','Y',0,150,160,140,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (528,18,'action','random.seed(42)
global state_dict
global vocab_size
global head_dim
if not os.path.exists(''input.txt''):
    import urllib.request
    names_url = ''https://raw.githubusercontent.com/karpathy/makemore/988aa59/names.txt''
    urllib.request.urlretrieve(names_url, ''input.txt'')
docs = [line.strip() for line in open(''input.txt'') if line.strip()]
random.shuffle(docs)
print(f''num docs: {len(docs)}'')
uchars = sorted(set(''''.join(docs)))
BOS = len(uchars)
vocab_size = len(uchars) + 1
print(f''vocab size: {vocab_size}'')
n_layer = 1
n_embd = 16
block_size = 16
n_head = 4
head_dim = n_embd // n_head
matrix = lambda nout, nin, std=0.08: [[Value(random.gauss(0, std)) for _ in range(nin)] for _ in range(nout)]
state_dict = {''wte'': matrix(vocab_size, n_embd), ''wpe'': matrix(block_size, n_embd), ''lm_head'': matrix(vocab_size, n_embd)}
params = [p for mat in state_dict.values() for row in mat for p in row]
learning_rate, beta1, beta2, eps_adam = (0.01, 0.85, 0.99, 1e-08)
m = [0.0] * len(params)
v = [0.0] * len(params)
num_steps = 1000
temperature = 0.5
print(''\n--- inference (new, hallucinated names) ---'')
if __name__ == ''__main__'':
    pass',0,150,280,180,80,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (529,18,'address','I_P',0,150,420,140,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (530,18,'vertical','',0,500,120,0,400,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (531,18,'branch','I_P',0,500,160,140,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (532,18,'action','FOR i in range(n_layer)
CALL U',0,500,280,180,80,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (533,18,'address','S_F',0,500,420,140,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (534,18,'vertical','',0,850,120,0,400,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (535,18,'branch','S_F',0,850,160,140,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (536,18,'action','FOR step in range(num_steps)
CALL A',0,850,280,180,80,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (537,18,'address','H_K',0,850,420,140,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (538,18,'vertical','',0,1200,120,0,400,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (539,18,'branch','H_K',0,1200,160,140,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (540,18,'action','FOR sample_idx in range(20)
CALL G',0,1200,280,180,80,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (541,18,'address','Конец',0,1200,420,140,30,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (881,19,'beginend','rmsnorm',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (882,19,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (883,19,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (884,19,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (885,19,'action','x',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (886,19,'action','ms = sum((xi * xi for xi in x)) / len(x)
scale = (ms + 1e-05) ** (-0.5)
return [xi * scale for xi in x]',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (891,20,'beginend','softmax',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (892,20,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (893,20,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (894,20,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (895,20,'action','logits',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (896,20,'action','max_val = max((val.data for val in logits))
exps = [(val - max_val).exp() for val in logits]
total = sum(exps)
return [e / total for e in exps]',0,170,170,110,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (897,21,'beginend','aaa',0,170,60,100,20,60,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (898,21,'beginend','Конец',0,660,510,60,20,60,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (899,21,'vertical','',0,170,80,0,520,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (900,21,'vertical','',0,420,120,0,480,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (901,21,'vertical','',0,660,120,0,380,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (902,21,'horizontal','',0,170,120,490,0,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (903,21,'arrow','',0,20,120,150,480,400,1,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (904,21,'branch','branch 1',0,170,170,50,30,60,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (905,21,'address','branch 2',0,170,550,50,30,60,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (906,21,'branch','branch 2',0,420,170,50,30,60,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (907,21,'branch','branch 3',0,660,170,50,30,60,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (908,21,'address','branch 3',0,420,550,50,30,60,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (909,21,'horizontal',NULL,0,170,60,200,0,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (910,21,'action',NULL,0,370,60,60,30,0,0,NULL,NULL,NULL,NULL);
CREATE TABLE info (key text primary key, value text);
INSERT INTO `info` (key,value) VALUES ('type','drakon');
INSERT INTO `info` (key,value) VALUES ('version','33');
INSERT INTO `info` (key,value) VALUES ('start_version','1');
INSERT INTO `info` (key,value) VALUES ('language','Python 3.x');
CREATE TABLE diagrams (diagram_id integer primary key, name text unique, origin text, description text, zoom double);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (1,'__add__','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (2,'__init__','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (3,'__mul__','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (4,'__neg__','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (5,'__pow__','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (6,'__radd__','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (7,'__rmul__','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (8,'__rsub__','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (9,'__rtruediv__','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (10,'__sub__','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (11,'__truediv__','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (12,'backward','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (13,'exp','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (14,'log','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (15,'relu','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (16,'gpt','-300 0','auto silhouette gpt',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (17,'linear','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (18,'main','0 0','auto silhouette main',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (19,'rmsnorm','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (20,'softmax','0 250',NULL,100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (21,'aaa','0 0',NULL,100.0);
CREATE TABLE diagram_info (diagram_id integer, name text, value text, primary key (diagram_id, name));
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (1,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (1,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (2,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (2,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (3,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (3,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (4,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (4,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (5,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (5,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (6,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (6,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (7,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (7,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (8,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (8,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (9,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (9,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (10,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (10,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (11,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (11,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (12,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (12,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (13,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (13,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (14,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (14,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (15,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (15,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (16,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (16,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (17,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (17,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (18,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (18,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (19,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (19,'orientation','portrait');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (20,'papersize','a4');
INSERT INTO `diagram_info` (diagram_id,name,value) VALUES (20,'orientation','portrait');
COMMIT;
