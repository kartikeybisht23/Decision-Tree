def gini_score(groups,classes):
    total_count=sum([len(group) for group in groups])
    gini=0
    for group in groups:
        #print(group)
        len_class=len(group)
        if len_class==0:
            continue
        score=0
        for class_val in classes:
            class_count=len([row[-1] for row in group if row[-1]==class_val])
            #print(f"class{class_val} counted is {class_count}")
            score_class=((class_count)/(len_class))**2
            #print(f"score of class {class_val} is {score_class}")
            score+=score_class
            #print(f"score of group is {score}")
        gini+=(1-score)*(len_class/total_count)
    return gini
def split_data(data,feat,thres):
    left=[]
    right=[]
    for row in data:
        if row[feat]<thres:
            left.append(row)
        else:
            right.append(row)
    return left,right
def get_split_info(data):
    class_val=list(set([row[-1] for row in data]))
    node_idx,node_score,node_value,node_groups=1000,1000,1000,[]
    for feat in range(len(data[0])-1):
        for row in data:
            groups=split_data(data,feat,node_value)
            score=gini_score(groups,class_val)
            #print("feat :{} score {}".format(row[feat],score))
            if score<node_score:
                node_score=score
                node_idx=feat
                node_value=row[feat]
                node_groups=groups
    return {"node_idx":node_idx,"node_score":node_score,"node_value":node_value,"node_groups":node_groups}

def max_group(group):
    print("inside max_group")
    print(group)
    print("end")
    if len(group)==0:
        return 0
    else:
        classes=[row[-1] for row in group]
        return max(classes,key=classes.count)
def split_node(node,depth,max_depth,min_class):
    left,right=node["node_groups"]
    del node["node_groups"]
    if not right or not left:
        node["right"]=node["left"]=max_group(left+right)
        return
    if depth>=max_depth:
        node["left"]=max_group(left)
        node["right"]=max_group(right)
        return
    if len(left)<=min_class:
        node["left"]=max_group(left)
    else:
        node["left"]=get_split_info(left)
        split_node(node["left"],depth+1,max_depth,min_class)
    if len(right)<=min_class:
        node["right"]=max_group(right)
    else:
        node["right"]=get_split_info(right)
        split_node(node["right"],depth+1,max_depth,min_class)
dataset=[[2.77,1.78,0],
        [1.72,1.69,0],
        [3.67,2.81,0],
        [3.96,2.61,0],
        [2.99,2.20,0],
        [7.49,3.10,1],
        [9.002,3.339,1],
        [7.44,0.47,1],
        [10.12,3.13,1],
        [6.64,3.31,1]]
def build_tree(train,max_depth,min_class):
    depth=0
    root=get_split_info(train)
    split_node(root,depth,max_depth,min_class)
    return root
build_tree(dataset,1,1)    
            
