<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="icon" href="/static/img/logo.png" type="image/png">
    <title>Noscope</title>
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="/static/css/bootstrap.css" type="text/css" >
    <link rel="stylesheet" href="/static/vendors/linericon/style.css" type="text/css" >
    <link rel="stylesheet" href="/static/css/font-awesome.min.css" type="text/css" >
    <link rel="stylesheet" href="/static/vendors/owl-carousel/owl.carousel.min.css" type="text/css" >
    <link rel="stylesheet" href="/static/vendors/lightbox/simpleLightbox.css" type="text/css" >
    <link rel="stylesheet" href="/static/vendors/nice-select/css/nice-select.css" type="text/css" >
    <link rel="stylesheet" href="/static/vendors/animate-css/animate.css" type="text/css">
    <link rel="stylesheet" href="/static/vendors/popup/magnific-popup.css" type="text/css">
    <link rel="stylesheet" href="/static/vendors/flaticon/flaticon.css" type="text/css">
    <!-- main css -->
    <link rel="stylesheet" href="/static/css/style.css" type="text/css">
    <link rel="stylesheet" href="/static/css/responsive.css" type="text/css">
    </head>


  <body>

    <header class="header_area">
      <!--<div class="main_menu">
        <nav class="navbar navbar-expand-lg navbar-light">
    <div class="container box_1620">-->
    <!-- Brand and toggle get grouped for better mobile display -->
    <a class="navbar-brand logo_h" href="/views/index.html"><img src="/static/img/logo.png" width="50%" height="50%" alt=""></a>
    <br /><br />
    <!--<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    </button>
    </div>
        </nav>
    </div> -->
    </header>

  <!--================Home Banner Area =================-->
  <section class="home_banner_area">
    <div class="container box_1620" style="text-align:center">

    <h1>Select images to compare!</h1>
    <hr /><br />
    <table id="main_table" style="width:100%; text-align:left">
      <tbody>
        <tr>
          <td valign="top">
            <img src="./../static/img/blueface.png" alt="Before" style="width:100%;border-radius: 20px; border-width:50px;padding-right:40px">
          </td>
          <td valign="top">
            <form action="/welcome.php" method="post">
              <h3>Before</h3>
              <input type="file" name="fileupload1" value="fileupload" id="fileupload" />
              <br /><br />
              <h3>After</h3>
              <input type="file" name="fileupload2" value="fileupload" id="fileupload" />
              <br /><br />
              <h3>Color Mode</h3>
              <p>Enter "rgb" or "rnd".</p>
              <input type="text" name="color" value="rgb">
              <br /><br />
              <h3>Griddify</h3>
              Griddify? <input type="checkbox" name="griddify" value="blah">
              <br /><br />
              <input value="Compare" type="submit" />
            </form>
          </td>
        </tr>
      </tbody>
    </table>

  </div>
  </section>

        <!--================Footer Area =================-->
        <footer class="footer_area p_120">
          <div class="container">
            <div class="row footer_inner">
              <div class="col-lg-5 col-sm-6">
                <aside class="f_widget news_widget">
                  <div class="f_title">
                    <h3>More About Noscope</h3>
                  </div>
                  <p>Noscope was created by a couple of hackers in order to solve property damage and retail issues. </p>

                </aside>
              </div>
            </div>
          </div>
        </footer>
        <!--================End Footer Area =================-->


    </body>
  </html>
