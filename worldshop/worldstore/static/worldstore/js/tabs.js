$(document).ready(function () {

 if (sessionStorage.getItem('tab') == '1'){
   $(".tabs-pills__item_active").removeClass(
      "tabs-pills__item_active line_active"
    );
     $($(".tab1").attr("href")).addClass("tabs-pills__item_active");
    $(".tab1").parent().addClass("tabs-pills__item_active line_active");
 }else if(sessionStorage.getItem('tab') == '2'){
    $(".tabs-pills__item_active").removeClass(
      "tabs-pills__item_active line_active"
    );
    $($(".tab2").attr("href")).addClass("tabs-pills__item_active");
    $(".tab2").parent().addClass("tabs-pills__item_active line_active");
 }else if (sessionStorage.getItem('tab') == '3'){
    $(".tabs-pills__item_active").removeClass(
      "tabs-pills__item_active line_active"
    );
    $($(".tab3").attr("href")).addClass("tabs-pills__item_active");
    $(".tab3").parent().addClass("tabs-pills__item_active line_active");
 }else{
     $(".tabs-pills__item_active").removeClass(
      "tabs-pills__item_active line_active"
    );
     $($(".tab1").attr("href")).addClass("tabs-pills__item_active");
    $(".tab1").parent().addClass("tabs-pills__item_active line_active");
 }

  $(".tabs-pills a").click(function (e) {
    e.preventDefault();
    $(".tabs-pills__item_active").removeClass(
      "tabs-pills__item_active line_active"
    );
    $(this).parent().addClass("tabs-pills__item_active line_active");
    $($(this).attr("href")).addClass("tabs-pills__item_active");
    sessionStorage.setItem('tab', $(this).attr("data-id"));
  });

  $(".login-registration__tabs-pills a").click(function (e) {
    e.preventDefault();
    $(".login-registration__item_active").removeClass(
      "login-registration__item_active"
    );
    $(this).parent().addClass("login-registration__item_active");
    $($(this).attr("href")).addClass("login-registration__item_active");
  });
});
/* npx browserslist@latest --update-db */
