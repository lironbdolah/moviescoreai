from os import path,system

def html(movies_summary,movie,image_url,top_review,images_path, summary_review, accuracy, name , output_path,start):
    barplot = path.join(images_path, 'barplot.png')
    file = open(path.join(output_path, name+".html"), "w")
    file.write('''<!DOCTYPE html> 
                    <html>    
                      <head>
                        <title>moviescoreai</title>
                        <link href="style.css" rel="stylesheet">
                        <script src="script.js" type="text/javascript"></script>
                        <style>     
                                h1 {font-size: 35px; }
                                h2 {font-size: 20px; align-items: center;}
                                h3 {font-size: 30px;}
                                h4 {font-size: 20px; }
                                h6 {font-size: 25px;}
                                    
                        
                                 body {
                                     background-color: #F9F8F1;
                                     color: #2C232A;
                                     font-family: sans-serif;
                                     font-size: 2.6em;
                                     margin: 0 auto;   
                                     width:1400px;  
                                      }
                    
                                    .container {
                                      display: flex;
                                      align-items: center;
                                      justify-content: right
                                      width: 1400px;
                                    }
                    
                    
                                    img{
                                      width: 825px;
                                      height: 425px;
                                      align-items: center;
                                      justify-content: center
                                    }
                                    
                                    .movie img:not(.movie) {
                                      display: block;
                                      margin-left: auto;
                                      margin-right: auto;
                                      width: 200px;
                                      height: 275px;
                                    }
                                    
                                    .image {
                                      flex-basis: 20%
                                    }
                                    
                                    .text {
                                      font-size: 16px;
                                      width: 600px;
                                    }
                                    
                                    .head{
                                    display: flex;
                                      align-items: center;
                                      justify-content: center
                                    } 
                                    
                                    .center {
                                      margin: auto;
                                      width: 20%;
                                      text-align: center;
                                    }
                                    
                                    .review {
                                      align-items: center;
                                      justify-content: center;
                                      font-size: 16px;
                                      font-size: 1.2vw;
                                      display: flex;
                                      }
                    
                        </style>
                      </head>
                      <body>
                        <div class="body">
                            <div class="center">
                                          <h1>moviescoreai</h1><br>
                                          <h2>Highest ranked movie:</h2>
                                          <h3>''' + movie + '''</h3>
                            </div>
                            <div class="movie">
                                          <img src='''+str(image_url)+'''>
                            </div> 
                            <div class="center"> 
                                <h6>Statistics:</h6>
                            </div> 
                            <div class="container">
                                <div class="image">
                                    <img src='''+str(barplot)+'''>
                                </div>
                                <div class="text">
                                    <p>'''+
                                    movies_summary + '''<br><br><br><br>
                                    Model Accuracy: ''' + str(accuracy) +'''% </p>
                                </div>
                            </div>
                            <div class="center">
                                <h4>Top Review:</h4>
                            </div>
                            <div class="review">
                                <p>''' + top_review + '''</p>
                            </div>
                            <br>
                            <div class="center">
                                <h4>Generated summary:</h4>
                            </div>
                            <div class="review">
                                <p>''' + summary_review + '''</p>
                            </div>
                      </body>
                    </html>''')
    file.close()
    if start:
        system("start " + path.join(output_path, 'moviescoreai.html'))

