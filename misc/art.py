groot = """
     .^. .  _    
    /: ||`\/ \~  ,       
  , [   &    / \ y'   
 {v':   `\   / `&~-,  
'y. '    |`   .  ' /
 \   '  .       , y       
 v .        '     v       
 V  .~.      .~.  V       
 : (  0)    (  0) :       
  i `'`      `'` j        
   i     __    ,j         
    `%`~....~'&           
 <~o' /  \/` \-s,
  o.~'.  )(  r  .o ,.
 o',  %``\/``& : 'bF  
d', ,ri.~~-~.ri , +h  
`oso' d`~..~`b 'sos`  
     d`+ II +`b              
     i_:_yi_;_y    
"""
broot = """







  _                     _    
 | |__  _ __ ___   ___ | |_  
 | '_ \| '__/ _ \ / _ \| __| 
 | |_) | | | (_) | (_) | |_  
 |_.__/|_|  \___/ \___/ \__| 






                            """

art = (groot, broot)
banner = '\n'.join(' '.join(pair) for pair in zip(*(s.split('\n') for s in art)))
