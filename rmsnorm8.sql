BEGIN TRANSACTION;
CREATE TABLE tree_nodes (node_id integer primary key, parent integer, type text, name text, diagram_id integer);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (1,0,'folder','microgpt',NULL);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (2,1,'folder','Value',NULL);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (3,1,'item','gpt',1);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (4,1,'item','linear',2);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (5,1,'item','main',3);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (6,1,'item','rmsnorm',4);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (7,1,'item','softmax',5);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (8,2,'item','',6);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (9,2,'item','',7);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (10,2,'item','',8);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (11,2,'item','',9);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (12,2,'item','',10);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (13,2,'item','',11);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (14,2,'item','',12);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (15,2,'item','',13);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (16,2,'item','',14);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (17,2,'item','',15);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (18,2,'item','',16);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (19,2,'item','',17);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (20,2,'item','',18);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (21,2,'item','',19);
INSERT INTO `tree_nodes` (node_id,parent,type,name,diagram_id) VALUES (22,2,'item','',20);
CREATE TABLE state (row integer primary key, current_dia integer, description text);
INSERT INTO `state` (row,current_dia,description) VALUES (1,5,'=== header ===
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
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (1,1,'beginend','gpt',1,500,420,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (2,1,'beginend','Конец',1,500,750,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (3,1,'action','global n_layer
global n_head
global head_dim
tok_emb = state_dict[''wte''][token_id]
pos_emb = state_dict[''wpe''][pos_id]
x = [t + p for t, p in zip(tok_emb, pos_emb)]
x = rmsnorm(x)
for li in range(n_layer):
    x_residual = x
    x = rmsnorm(x)
    q = linear(x, state_dict[f''layer{li}.attn_wq''])
    k = linear(x, state_dict[f''layer{li}.attn_wk''])
    v = linear(x, state_dict[f''layer{li}.attn_wv''])
    keys[li].append(k)
    values[li].append(v)
    x_attn = []
    for h in range(n_head):
        hs = h * head_dim
        q_h = q[hs:hs + head_dim]
        k_h = [ki[hs:hs + head_dim] for ki in keys[li]]
        v_h = [vi[hs:hs + head_dim] for vi in values[li]]
        attn_logits = [sum((q_h[j] * k_h[t][j] for j in range(head_dim))) / head_dim ** 0.5 for t in range(len(k_h))]
        attn_weights = softmax(attn_logits)
        head_out = [sum((attn_weights[t] * v_h[t][j] for t in range(len(v_h)))) for j in range(head_dim)]
        x_attn.extend(head_out)
    x = linear(x_attn, state_dict[f''layer{li}.attn_wo''])
    x = [a + b for a, b in zip(x, x_residual)]
    x_residual = x
    x = rmsnorm(x)
    x = linear(x, state_dict[f''layer{li}.mlp_fc1''])
    x = [xi.relu() for xi in x]
    x = linear(x, state_dict[f''layer{li}.mlp_fc2''])
    x = [a + b for a, b in zip(x, x_residual)]
logits = linear(x, state_dict[''lm_head''])
return logits',1,500,550,170,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (4,1,'vertical','',1,500,420,0,340,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (5,1,'horizontal','',1,530,420,140,0,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (6,1,'action','token_id, pos_id, keys, values',1,690,420,50,20,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (7,2,'beginend','linear',0,170,20,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (8,2,'beginend','Конец',0,170,350,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (9,2,'action','return [sum((wi * xi for wi, xi in zip(wo, x))) for wo in w]',0,170,150,170,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (10,2,'vertical','',0,170,20,0,340,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (11,2,'horizontal','',0,200,20,140,0,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (12,2,'action','x, w',0,360,20,50,20,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (13,3,'beginend','main',0,170,20,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (14,3,'beginend','Конец',0,170,350,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (15,3,'action','random.seed(42)
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
for i in range(n_layer):
    state_dict[f''layer{i}.attn_wq''] = matrix(n_embd, n_embd)
    state_dict[f''layer{i}.attn_wk''] = matrix(n_embd, n_embd)
    state_dict[f''layer{i}.attn_wv''] = matrix(n_embd, n_embd)
    state_dict[f''layer{i}.attn_wo''] = matrix(n_embd, n_embd)
    state_dict[f''layer{i}.mlp_fc1''] = matrix(4 * n_embd, n_embd)
    state_dict[f''layer{i}.mlp_fc2''] = matrix(n_embd, 4 * n_embd)
params = [p for mat in state_dict.values() for row in mat for p in row]
learning_rate, beta1, beta2, eps_adam = (0.01, 0.85, 0.99, 1e-08)
m = [0.0] * len(params)
v = [0.0] * len(params)
num_steps = 1000
for step in range(num_steps):
    doc = docs[step % len(docs)]
    tokens = [BOS] + [uchars.index(ch) for ch in doc] + [BOS]
    n = min(block_size, len(tokens) - 1)
    keys, values = ([[] for _ in range(n_layer)], [[] for _ in range(n_layer)])
    losses = []
    for pos_id in range(n):
        token_id, target_id = (tokens[pos_id], tokens[pos_id + 1])
        logits = gpt(token_id, pos_id, keys, values)
        probs = softmax(logits)
        loss_t = -probs[target_id].log()
        losses.append(loss_t)
    loss = 1 / n * sum(losses)
    loss.backward()
    lr_t = learning_rate * (1 - step / num_steps)
    for i, p in enumerate(params):
        m[i] = beta1 * m[i] + (1 - beta1) * p.grad
        v[i] = beta2 * v[i] + (1 - beta2) * p.grad ** 2
        m_hat = m[i] / (1 - beta1 ** (step + 1))
        v_hat = v[i] / (1 - beta2 ** (step + 1))
        p.data -= lr_t * m_hat / (v_hat ** 0.5 + eps_adam)
        p.grad = 0
    print(f''step {step + 1:4d} / {num_steps:4d} | loss {loss.data:.4f}'', end=''\r'')
temperature = 0.5
print(''\n--- inference (new, hallucinated names) ---'')
for sample_idx in range(20):
    keys, values = ([[] for _ in range(n_layer)], [[] for _ in range(n_layer)])
    token_id = BOS
    sample = []
    for pos_id in range(block_size):
        logits = gpt(token_id, pos_id, keys, values)
        probs = softmax([l / temperature for l in logits])
        token_id = random.choices(range(vocab_size), weights=[p.data for p in probs])[0]
        if token_id == BOS:
            break
        sample.append(uchars[token_id])
    print(f"sample {sample_idx + 1:2d}: {''''.join(sample)}")
if __name__ == ''__main__'':
    pass',0,170,150,170,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (16,3,'vertical','',0,170,20,0,340,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (19,4,'beginend','rmsnorm',0,170,20,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (20,4,'beginend','Конец',0,170,350,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (21,4,'action','ms = sum((xi * xi for xi in x)) / len(x)
scale = (ms + 1e-05) ** (-0.5)
return [xi * scale for xi in x]',0,170,150,170,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (22,4,'vertical','',0,170,20,0,340,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (23,4,'horizontal','',0,200,20,140,0,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (24,4,'action','x',0,360,20,50,20,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (25,5,'beginend','softmax',0,170,20,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (26,5,'beginend','Конец',0,170,350,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (27,5,'action','max_val = max((val.data for val in logits))
exps = [(val - max_val).exp() for val in logits]
total = sum(exps)
return [e / total for e in exps]',0,170,150,170,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (28,5,'vertical','',0,170,20,0,340,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (29,5,'horizontal','',0,200,20,140,0,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (30,5,'action','logits',0,360,20,50,20,0,0,NULL,NULL,NULL,NULL);
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (31,6,'beginend','__add__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (32,6,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (33,6,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (34,6,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (35,6,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (36,6,'action','if isinstance(other, Value):
    other = other
else:
    other = Value(other)
return Value(self.data + other.data, (self, other), (1, 1))',0,170,170,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (37,6,'commentout','Note that the argument list starts with
#comment
This makes the current procedure 
to be added as a method to the class.',0,610,60,170,50,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (38,6,'commentin','In order to make the code generator create a class,
add something like this to the File description:

=== class ===
class Sorter

Only one class per file is supported.',0,570,260,228,70,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (39,7,'beginend','__init__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (40,7,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (41,7,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (42,7,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (43,7,'action','#method
self
data
children
local_grads',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (44,7,'action','self.data = data
self.grad = 0
self._children = children
self._local_grads = local_grads',0,170,170,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (45,7,'commentout','Note that the argument list starts with
#comment
This makes the current procedure 
to be added as a method to the class.',0,610,60,170,50,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (46,7,'commentin','In order to make the code generator create a class,
add something like this to the File description:

=== class ===
class Sorter

Only one class per file is supported.',0,570,260,228,70,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (47,8,'beginend','__mul__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (48,8,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (49,8,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (50,8,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (51,8,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (52,8,'action','if isinstance(other, Value):
    other = other
else:
    other = Value(other)
return Value(self.data * other.data, (self, other), (other.data, self.data))',0,170,170,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (53,8,'commentout','Note that the argument list starts with
#comment
This makes the current procedure 
to be added as a method to the class.',0,610,60,170,50,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (54,8,'commentin','In order to make the code generator create a class,
add something like this to the File description:

=== class ===
class Sorter

Only one class per file is supported.',0,570,260,228,70,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (55,9,'beginend','__neg__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (56,9,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (57,9,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (58,9,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (59,9,'action','#method
self',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (60,9,'action','return self * -1',0,170,170,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (61,9,'commentout','Note that the argument list starts with
#comment
This makes the current procedure 
to be added as a method to the class.',0,610,60,170,50,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (62,9,'commentin','In order to make the code generator create a class,
add something like this to the File description:

=== class ===
class Sorter

Only one class per file is supported.',0,570,260,228,70,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (63,10,'beginend','__pow__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (64,10,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (65,10,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (66,10,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (67,10,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (68,10,'action','return Value(self.data ** other, (self,), (other * self.data ** (other - 1),))',0,170,170,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (69,10,'commentout','Note that the argument list starts with
#comment
This makes the current procedure 
to be added as a method to the class.',0,610,60,170,50,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (70,10,'commentin','In order to make the code generator create a class,
add something like this to the File description:

=== class ===
class Sorter

Only one class per file is supported.',0,570,260,228,70,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (71,11,'beginend','__radd__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (72,11,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (73,11,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (74,11,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (75,11,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (76,11,'action','return self + other',0,170,170,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (77,11,'commentout','Note that the argument list starts with
#comment
This makes the current procedure 
to be added as a method to the class.',0,610,60,170,50,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (78,11,'commentin','In order to make the code generator create a class,
add something like this to the File description:

=== class ===
class Sorter

Only one class per file is supported.',0,570,260,228,70,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (79,12,'beginend','__rmul__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (80,12,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (81,12,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (82,12,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (83,12,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (84,12,'action','return self * other',0,170,170,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (85,12,'commentout','Note that the argument list starts with
#comment
This makes the current procedure 
to be added as a method to the class.',0,610,60,170,50,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (86,12,'commentin','In order to make the code generator create a class,
add something like this to the File description:

=== class ===
class Sorter

Only one class per file is supported.',0,570,260,228,70,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (87,13,'beginend','__rsub__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (88,13,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (89,13,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (90,13,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (91,13,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (92,13,'action','return other + -self',0,170,170,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (93,13,'commentout','Note that the argument list starts with
#comment
This makes the current procedure 
to be added as a method to the class.',0,610,60,170,50,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (94,13,'commentin','In order to make the code generator create a class,
add something like this to the File description:

=== class ===
class Sorter

Only one class per file is supported.',0,570,260,228,70,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (95,14,'beginend','__rtruediv__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (96,14,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (97,14,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (98,14,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (99,14,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (100,14,'action','return other * self ** (-1)',0,170,170,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (101,14,'commentout','Note that the argument list starts with
#comment
This makes the current procedure 
to be added as a method to the class.',0,610,60,170,50,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (102,14,'commentin','In order to make the code generator create a class,
add something like this to the File description:

=== class ===
class Sorter

Only one class per file is supported.',0,570,260,228,70,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (103,15,'beginend','__sub__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (104,15,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (105,15,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (106,15,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (107,15,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (108,15,'action','return self + -other',0,170,170,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (109,15,'commentout','Note that the argument list starts with
#comment
This makes the current procedure 
to be added as a method to the class.',0,610,60,170,50,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (110,15,'commentin','In order to make the code generator create a class,
add something like this to the File description:

=== class ===
class Sorter

Only one class per file is supported.',0,570,260,228,70,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (111,16,'beginend','__truediv__',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (112,16,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (113,16,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (114,16,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (115,16,'action','#method
self
other',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (116,16,'action','return self * other ** (-1)',0,170,170,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (117,16,'commentout','Note that the argument list starts with
#comment
This makes the current procedure 
to be added as a method to the class.',0,610,60,170,50,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (118,16,'commentin','In order to make the code generator create a class,
add something like this to the File description:

=== class ===
class Sorter

Only one class per file is supported.',0,570,260,228,70,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (119,17,'beginend','backward',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (120,17,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (121,17,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (122,17,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (123,17,'action','#method
self',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (124,17,'action','topo = []
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
        child.grad += local_grad * v.grad',0,170,170,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (125,17,'commentout','Note that the argument list starts with
#comment
This makes the current procedure 
to be added as a method to the class.',0,610,60,170,50,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (126,17,'commentin','In order to make the code generator create a class,
add something like this to the File description:

=== class ===
class Sorter

Only one class per file is supported.',0,570,260,228,70,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (127,18,'beginend','exp',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (128,18,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (129,18,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (130,18,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (131,18,'action','#method
self',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (132,18,'action','return Value(math.exp(self.data), (self,), (math.exp(self.data),))',0,170,170,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (133,18,'commentout','Note that the argument list starts with
#comment
This makes the current procedure 
to be added as a method to the class.',0,610,60,170,50,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (134,18,'commentin','In order to make the code generator create a class,
add something like this to the File description:

=== class ===
class Sorter

Only one class per file is supported.',0,570,260,228,70,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (135,19,'beginend','log',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (136,19,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (137,19,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (138,19,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (139,19,'action','#method
self',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (140,19,'action','return Value(math.log(self.data), (self,), (1 / self.data,))',0,170,170,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (141,19,'commentout','Note that the argument list starts with
#comment
This makes the current procedure 
to be added as a method to the class.',0,610,60,170,50,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (142,19,'commentin','In order to make the code generator create a class,
add something like this to the File description:

=== class ===
class Sorter

Only one class per file is supported.',0,570,260,228,70,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (143,20,'beginend','relu',0,170,60,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (144,20,'beginend','End',0,170,390,50,20,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (145,20,'vertical','',0,170,80,0,290,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (146,20,'horizontal','',0,200,60,80,0,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (147,20,'action','#method
self',0,310,60,50,40,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (148,20,'action','return Value(max(0, self.data), (self,), (float(self.data > 0),))',0,170,170,110,20,0,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (149,20,'commentout','Note that the argument list starts with
#comment
This makes the current procedure 
to be added as a method to the class.',0,610,60,170,50,60,0,NULL,'',NULL,'');
INSERT INTO `items` (item_id,diagram_id,type,text,selected,x,y,w,h,a,b,aux_value,color,format,text2) VALUES (150,20,'commentin','In order to make the code generator create a class,
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
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (1,'gpt','0 250',NULL,120.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (2,'linear','-41 -82',NULL,120.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (3,'main','-41 -82',NULL,120.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (4,'rmsnorm','-41 -82',NULL,120.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (5,'softmax','-41 -82',NULL,120.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (6,'__add__','24 -13','',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (7,'__init__','24 -13','The constructor of class Sorter.',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (8,'__mul__','24 -13','',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (9,'__neg__','24 -13','',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (10,'__pow__','24 -13','',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (11,'__radd__','24 -13','',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (12,'__rmul__','24 -13','',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (13,'__rsub__','24 -13','',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (14,'__rtruediv__','24 -13','',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (15,'__sub__','24 -13','',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (16,'__truediv__','24 -13','',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (17,'backward','24 -13','',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (18,'exp','24 -13','',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (19,'log','24 -13','',100.0);
INSERT INTO `diagrams` (diagram_id,name,origin,description,zoom) VALUES (20,'relu','24 -13','',100.0);
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
