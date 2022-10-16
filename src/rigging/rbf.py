
import numpy as np

#------------


class RBF:

    def __init__(self,eps=2.0 ):

        self.eps = eps
        self.max_dist = 0.01
        self.pose_list = []
        self.value_list = []


    def append_pose_list(self,new_pose):
        self.pose_list.append(new_pose)
    
    def append_value_list(self,new_value):
        self.value_list.append(new_value)


    def get_radius_mat(self):
        
        # get n*n*3 matrix

        #first gen the original pose_list n*n matrix
        ori_mat = np.full((len(self.pose_list),len(self.pose_list),3),self.pose_list)

        #transpose 
        trans_mat = np.transpose(ori_mat,(1,0,2)) 

        # get the sub
        sub_mat = np.sqrt((ori_mat - trans_mat)**2) 
        
        # get distance matrix
        dist_mat = np.linalg.norm(sub_mat,axis=2) 

        self.max_dist = dist_mat.max()

        #normalize to 0 ,1
        return( dist_mat / self.max_dist )



    def get_likeness_mat(self,radius):

        #use gauss rbf function to gen likeness mat

        return np.exp( -( self.eps * radius)**2 )


    def compute_weight(self):

        radius_mat = self.get_radius_mat()
        likeness_mat = self.get_likeness_mat(radius_mat)

        w = np.linalg.solve(likeness_mat , self.value_list)

        return(w)


    def __call__(self,new_x):

        w = self.compute_weight()

        temp_radius_mat = []

        for i in range(len(self.pose_list)):

            dist = np.sqrt(np.sum((self.pose_list[i] - new_x[0])**2)) / self.max_dist
            temp_radius_mat.append(dist)
        
        
        temp_likeness_mat = self.get_likeness_mat(np.array(temp_radius_mat))

        return np.dot(temp_likeness_mat,w)


if (__name__ == '__main__'):

    # define

    arr1 = [[4.857,3.438,1.03],[-1.926,3.917,-0.404],[-1.308,1.773,6.114],[3.65,3.762,5.581]]
    y = np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1]])

    rbf_node = RBF(eps = 2.0)

    for i in arr1:
        rbf_node.append_pose_list(i)

    for i in y:
        rbf_node.append_value_list(i)

    # run 

    new_pose = np.array([[4.2,3.5,3.35]])
    result = rbf_node(new_pose)
    print(result)
