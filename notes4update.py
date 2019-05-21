

'''

#testing if the parge file is a problem, does not appear to be the case


import zlib
           dirpath = tempfile.mkdtemp()   
           print ('Updating: ',name_full)
           print dirpath


           #make directory if it does not exist
           if not os.path.isdir(__location__+dirchain):       
               os.makedirs(__location__+dirchain)

           #local logfile
           plog = open(__location__+dirchain+'/%s'%"diff.log", "a")
           plog.write("\n############ %s-%s ############\n"%(datetime.now().strftime('%Y-%m-%d'),nsplit[-1]))
           
           # Download file to temporary folder
           try:
               r = requests.get(d_url)
               z = zipfile.ZipFile(io.BytesIO(r.content))
               z.extractall(dirpath)
           except NotImplementedError:
               
               response = requests.get(d_url, stream=True)
               handle = open(dirpath+'zip', "wb")
               for chunk in response.iter_content(chunk_size=512):
                   if chunk:  # filter out keep-alive new chunks
                       handle.write(chunk)
               handle.close()
               
               #r = requests.get(d_url)            
               src = open( dirpath+'/zip', "rb" )
               zf = zipfile.ZipFile( io.BytesIO(r.content) )
               for m in  zf.infolist():

                   # Examine the header
                   print m.filename, m.header_offset, m.compress_size, repr(m.extra), repr(m.comment)
                   src.seek( m.header_offset )
                   src.read( 30 ) # Good to use struct to unpack this.
                   nm= src.read( len(m.filename) )
                   if len(m.extra) > 0: ex= src.read( len(m.extra) )
                   if len(m.comment) > 0: cm= src.read( len(m.comment) ) 

                   # Build a decompression object
                   decomp= zlib.decompressobj(-15)

                   # This can be done with a loop reading blocks
                   out= open( m.filename, "wb" )
                   result= decomp.decompress( src.read( m.compress_size ) )
                   out.write( result )
                   result = decomp.flush()
                   out.write( result )
                   # end of the loop
                   out.close()

               zf.close()
               src.close()

           if verbose: print (dirpath,'->',final_loc) #, os.listdir(dirpath)
           files = glob.glob(dirpath+'\\*.%s'%ftype)
           if len(files) >1: 
               warnings.warn("Warning: More than one file detected for %s. Only the first has been used."%name)

        
           #read the updated file
           new = open(files[0],'r').readlines()

           if os.path.exists(final_loc):
                   old = open(final_loc,'r').readlines()
                   for line in difflib.unified_diff(new, old, fromfile=
   datetime.now().strftime('%H:%M:%S')+'_new', tofile='%s_old'%name, lineterm=''):
                       plog.write(line)
                   mainlog.write('Updating: %s - %s\n'%(name_full,final_loc) )
           else:
               plog.write('\n Created '+name)
               mainlog.write('Adding: %s - %s\n'%(name_full,final_loc) )


           
           plog.close()

           #error: Error -3 while decompressing: too many length or distance symbols
           '''


# In[10]:


'''
#view all names
n = []
for i in current:
    n.append(current[i]['DatasetName'])
    
n.sort()
for i in n:
    print i
'''


