import h5py


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

path = "."
fout = open("rmse.csv", "w")

nrea_compare = 100

for i1 in range(len(structures)):
    
    clust = structures[i1].split('_')
    file_path = path + '/' + structures[i1] + '/spin_mc_red.h5'
    hf_i = h5py.File(file_path, 'r')
    nrea_i = hf_i.attrs['num_realisations']
    
    for j1 in range(i1+1, len(structures)):

        print(structures[i1] + "\t" + structures[j1])
        clust = structures[j1].split('_')
        file_path = path + '/' + structures[j1] + '/spin_mc_red.h5'
        hf_j = h5py.File(file_path, 'r')
        nrea_j = hf_j.attrs['num_realisations']

        #for i2 in range(nrea_i):
        for i2 in range(nrea_compare):

            mtdata_i = hf_i[str(i2) + '/mt'] # transition matrix

            t_i = mtdata_i[:, 0]
            m_i = mtdata_i[:, 1]

            #for j2 in range(nrea_j):
            for j2 in range(nrea_compare):

                mtdata_j = hf_j[str(j2) + '/mt'] # transition matrix

                t_j = mtdata_j[:, 0]
                m_j = mtdata_j[:, 1]    

                rmse = sum((m_i - m_j)**2)
                
                fout.write(structures[i1] + ', ' +
                           structures[j1] + ', ' +
                           str(i2) + ', ' +
                           str(j2) + ', ' +
                           str(rmse) + "\n")        

        hf_j.close()
    hf_i.close()
fout.close()
