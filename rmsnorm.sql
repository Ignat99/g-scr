BEGIN TRANSACTION;
CREATE TABLE tree_nodes (
                node_id INTEGER PRIMARY KEY,
                parent_id INTEGER,
                name TEXT,
                type TEXT,
                diagram_id INTEGER
            );
INSERT INTO `tree_nodes` (node_id,parent_id,name,type,diagram_id) VALUES (1,0,'rmsnorm_project','folder',NULL);
INSERT INTO `tree_nodes` (node_id,parent_id,name,type,diagram_id) VALUES (2,1,'rmsnorm','diagram',1);
CREATE TABLE state (p TEXT, v TEXT);
CREATE TABLE items (
                item_id INTEGER PRIMARY KEY,
                diagram_id INTEGER,
                type TEXT,
                text TEXT,
                x INTEGER,
                y INTEGER,
                w INTEGER,
                h INTEGER,
                flag1 INTEGER,
                flag2 INTEGER,
                text2 TEXT,
                link_type TEXT,
                line_to INTEGER
            );
INSERT INTO `items` (item_id,diagram_id,type,text,x,y,w,h,flag1,flag2,text2,link_type,line_to) VALUES (1,1,'header','rmsnorm(x)',160,60,100,40,NULL,NULL,NULL,NULL,2);
INSERT INTO `items` (item_id,diagram_id,type,text,x,y,w,h,flag1,flag2,text2,link_type,line_to) VALUES (2,1,'action','ms = sum((xi * xi for xi in x)) / len(x)
scale = (ms + 1e-05) ** (-0.5)',160,150,240,60,NULL,NULL,NULL,NULL,3);
INSERT INTO `items` (item_id,diagram_id,type,text,x,y,w,h,flag1,flag2,text2,link_type,line_to) VALUES (3,1,'end','return [xi * scale for xi in x]',160,250,220,40,NULL,NULL,NULL,NULL,NULL);
CREATE TABLE info (p TEXT, v TEXT);
INSERT INTO `info` (p,v) VALUES ('version','1.33');
INSERT INTO `info` (p,v) VALUES ('type','drakon');
CREATE TABLE diagrams (
                diagram_id INTEGER PRIMARY KEY,
                name TEXT,
                origin TEXT,
                description TEXT,
                zoom DOUBLE
            );
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (1,'rmsnorm','python','',1.0);
CREATE TABLE diagram_info (diagram_id INTEGER, p TEXT, v TEXT);
COMMIT;
