import os


structures = ['npStruct_2p_Ychain',
              'npStruct_2p_Zchain',
              'npStruct_2p_arkus',
              'npStruct_3p_Ychain',
              'npStruct_3p_Zchain',
              'npStruct_3p_arkus',
              'npStruct_3p_arkusXZ',
              'npStruct_4p_Ychain',
              'npStruct_4p_Zchain',
              'npStruct_4p_arkus',
              'npStruct_4p_ring',
              'npStruct_4p_ringXZ',
              'npStruct_4p_triangle',
              'npStruct_4p_triangleXZ',
              'npStruct_5p_Ychain',
              'npStruct_5p_Zchain',
              'npStruct_5p_arkus',
              'npStruct_5p_pyramide',
              'npStruct_5p_ring',
              'npStruct_5p_ringXZ',
              'npStruct_5p_triangle',
              'npStruct_5p_triangleXZ',
              'npStruct_6p1_arkus',
              'npStruct_6p2_arkus',
              'npStruct_6p_Ychain',
              'npStruct_6p_Zchain',
              'npStruct_6p_ring',
              'npStruct_6p_ringXZ',
              'npStruct_6p_triangle',
              'npStruct_6p_triangleXZ',
              'npStruct_7p1_arkus',
              'npStruct_7p2_arkus',
              'npStruct_7p3_arkus',
              'npStruct_7p4_arkus',
              'npStruct_7p5_arkus',
              'npStruct_7p_Ychain',
              'npStruct_7p_Zchain',
              'npStruct_7p_ring',
              'npStruct_7p_ringXZ',
              'npStruct_7p_triangle',
              'npStruct_7p_triangleXZ',
              'npStruct_1p_nonint']


#######################################################################
#######################################################################
#######################################################################

path = "."

for i in structures:
    
    print(i)

    clust = i.split('_')

    file_path = path + '/' + i
    
    os.chdir(file_path)
    
    filename =  'spin_mc.h5'
    try:
        os.remove(filename)
    except OSError:
        print("No file {}".format(filename))
    
    os.chdir('../')

