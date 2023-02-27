$(document).ready(function () {

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

  // Настройка AJAX
  $(function () {
    $.ajaxSetup({
      headers: { "X-CSRFToken": getCookie("csrftoken") },
    });
  });

// Лайки
function like()
{
    var like = $(this);
    var type = like.data('type');
    var pk = like.data('id');
    var action = like.data('action');
    var dislike = like.next();

    $.ajax({
        url : "/api/" + type +"/" + pk + "/" + action + "/",
        type : 'POST',
        data : { 'obj' : pk },
        xhrFields: {
            withCredentials: true,
        },

        success : function (json) {
           like.find("[data-count='like']").text(json.like_count);
           dislike.find("[data-count='dislike']").text(json.dislike_count);
        }
    });

    return false;
}



function dislike()
{
    var dislike = $(this);
    var type = dislike.data('type');
    var pk = dislike.data('id');
    var action = dislike.data('action');
    var like = dislike.prev();

    $.ajax({
        url : "/api/" + type +"/" + pk + "/" + action + "/",
        type : 'POST',
        data : { 'obj' : pk },
        xhrFields: {
            withCredentials: true,
        },

        success : function (json) {
            dislike.find("[data-count='dislike']").text(json.dislike_count); // .toggleClass('is-active')
            like.find("[data-count='like']").text(json.like_count);
        }
    });

    return false;
}

// Подключение обработчиков
$(function() {
    $('[data-action="like"]').click(like);
    $('[data-action="dislike"]').click(dislike);
  });


// Закладки
//bookmarkStorage = window.localStorage;
//
//function to_bookmarks()
//{
//    var current = $(this);
//    var type = current.data('type');
//    var pk = current.data('id');
//    var action = current.data('action');
//
//    $.ajax({
//        url : "/api/" + type + "/" + pk + "/" + action + "/",
//        type : 'POST',
//        data : { 'obj' : pk },
//
//        success : function (json) {
//            current.find("[data-count='" + action + "']").text(json.count);
//        }
//    });
//
//    return false;
//}
//
//// Подключение обработчика
//$(function() {
//    $('[data-action="bookmark"]').click(to_bookmarks);
//});
const add_to_favorites_url = '/favorites/add/'
const remove_from_favorites_url = '/favorites/remove/'
const favorites_api_url = '/favorites/api/'
const added_to_favorites_class = 'added'

function add_to_favorites () {
    $('.add_to_favorites').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault()
            const type = $(el).data('type')
            const id = $(el).data('id')

            if($(e.target).parent().hasClass(added_to_favorites_class)){
                console.log('Удаляем из избранного');
                $.ajax({
                    url: remove_from_favorites_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        type: type,
                        id: id,
                    },
                    success: (data) => {
                        $(el).removeClass(added_to_favorites_class)
                        $(el).children()[0].classList.remove('fa-solid')
                        $(el).children()[0].classList.add('fa-regular')
                    }
                })
            } else{
                console.log('Добовляем в избранное');
                $.ajax({
                   url: add_to_favorites_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        type: type,
                        id: id,
                    },
                    success: (data) => {
                        $(el).addClass(added_to_favorites_class)
                        $(el).children()[0].classList.add('fa-solid')
                        $(el).children()[0].classList.remove('fa-regular')
                    }
                })
            }
        })
    })
}


function get_session_favorites() {

    $.getJSON(favorites_api_url, (json) =>{
        if(json !== null){
            for(let i = 0; i < json.length; i++){
                $('.add_to_favorites').each((index, el) => {
                    const type = $(el).data('type')
                    const id = $(el).data('id')

                    if(json[i].type == type && json[i].id == id){
                        $(el).addClass(added_to_favorites_class)
                        $(el).children()[0].classList.add('fa-solid')
                        $(el).children()[0].classList.remove('fa-regular')
                    }
                })
            }
        }
    })
}

add_to_favorites()
get_session_favorites()


  /* СКРОЛИНГ НАВИГАЦИОННОГО МЕНЮ */

  var prevScrollpos = window.pageYOffset;
  window.onscroll = function () {
    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
      document.getElementById("navbar").style.top = "0";
    } else {
      document.getElementById("navbar").style.top = "-70px";
    }
    prevScrollpos = currentScrollPos;
  };

  /* НАВИГАЦИОННОЕ МЕНЮ МОБИЛЬНАЯ ВЕРСИЯ */
  // Burger

  $(".navbar_burger").on("click", function () {
    if (!$(this).hasClass("open")) {
      $(this).addClass("open");
      $("html").css("overflow-y", "hidden");
      $(".nav-block__menu").addClass("menu-open");
      $(".nav").addClass("fixed-top");
    } else {
      $(this).removeClass("open");
      $("html").css("overflow", "auto");
      $(".nav-block__menu").removeClass("menu-open");
      $(".nav").removeClass("fixed-top");
    }
  });


   /* ВЕРХНЕЕ НАВИГАЦИОННОЕ МЕНЮ МОБИЛЬНАЯ ВЕРСИЯ */

  $(".mobile-top-nav__burger").on("click", function () {
    if (!$(this).hasClass("open")) {
      $(this).addClass("open");
      $("html").css("overflow-y", "hidden");
      $(".mobile-top-navbar").animate(
        {
          left: 0,
        },
        500
      );
    } else {
      $(this).removeClass("open");
      $("html").css("overflow", "auto");
      $(".mobile-top-navbar").animate(
        {
          left: "-80%",
        },
        500
      );
    }
  });

  /* HEADER DROPDOWN */

  dropdown_list = [
    ".dropdown-region",
    ".dropdown-categories",
    ".dropdown-sort",
    ".filter__from",
    ".filter__to",
    ".menu-links-categories__toggle"
  ];

  dropdown_menu = [
    ".dropdown-region__menu",
    ".dropdown-categories__menu",
    ".dropdown-sort__menu",
    ".filter__from_menu",
    ".filter__to_menu",
    ".menu-links-categories__menu"
  ];

  for (let i = 0; i < dropdown_list.length; i++) {
    $(dropdown_list[i]).click(function () {
      for (let j = 0; j < dropdown_menu.length; j++) {
        if (j == i) {
          $(dropdown_menu[j]).slideToggle(150);
        }
      }
    });
  }
 /* HEADER DROPDOWN */
//    for(let i = 0; i < $(".add_to_favorites").length; i++){
//        if($(".add_to_favorites")[i].hasClass(added_to_favorites_class)){
//            $(".add_to_favorites")[i].children()[0].classList.remove("fa-regular");
//            $(".add_to_favorites")[i].children()[0].classList.add('fa-solid');
//        }else{
//            $(".add_to_favorites")[i].classList.remove("fa-solid");
//            $(".add_to_favorites")[i].classList.add("fa-regular");
//        }
//    }
//    if ($(".add_to_favorites").hasClass(added_to_favorites_class)) {
//        $(this).children()[0].classList.remove("fa-regular");
//        $(this).children()[0].classList.add('fa-solid');
//    } else{
//        $(this).children()[0].classList.remove("fa-solid");
//        $(this).children()[0].classList.add("fa-regular");
//    }
//  $(".favorite-link").click(function () {
//    if ($(this).hasClass(added_to_favorites_class)) {
//      $(this).children()[0].classList.remove("fa-regular");
//      $(this).children()[0].classList.add('fa-solid');
//    } else {
//      $(this).children()[0].classList.remove("fa-solid");
//      $(this).children()[0].classList.add("fa-regular");
//    }
//  });

//  localStorage.clear();

  // MODAL WINDOWS

  btns = [
    ".review-form__btn",
    ".about__btn-modal",
    ".about__btn-modal-geo",
    ".header-info__btn",
    ".tabs-card__delete",
    ".online_shop_share",
    ".product_share",
    ".mobile-version__contact",
    ".header-info__contact_us",
    ".search_btn",
    ".del-shop"
  ];

  modals = [
    ".review-form",
    ".content_form",
    ".geo-form",
    ".social-links-form",
    ".delete-product",
    ".online_shop_share_block_js",
    ".product_share_block",
    ".mobile-contacts-modal",
    ".profile-contacts-modal",
    ".filter-window",
    ".delete-online_shop"
  ];

  for (let i = 0; i < btns.length; i++) {
    $(btns[i]).click(function (e) {
      e.preventDefault();
      $(".overlay").show().css("overflow", "auto");
      $("html").css("overflow-y", "hidden");
      for (let j = 0; j < modals.length; j++) {
        if (j == i) {
          $(modals[j]).animate({
            top: "50%",
          });
        }
      }
    });
  }

  $(".overlay").click(function () {
    $(".overlay").hide();
    $("html").css("overflow-y", "scroll");
    for (let j = 0; j < modals.length; j++) {
      console.log(modals[j]);
      $(modals[j]).animate({
        top: "-150%",
      });
    }
  });

  // MODAL WINDOWS         TODO кое где добавить кнопочки закрывающие модальные окна
//
//  $(".review-form__btn").click(function (e) {
//    e.preventDefault();
//    $(".overlay").show().css("overflow", "auto");
//    $("html").css("overflow-y", "hidden");
//    $(".review-form").animate({
//      top: "50%",
//    });
//  });
//  // Выплывающее окно
//  $(".overlay").click(function () {
//    $(".overlay").hide();
//    $("html").css("overflow-y", "scroll");
//    $(".review-form").animate({
//      top: "-150%",
//    });
//  });
//
//  // content form
//  $(".about__btn-modal").click(function (e) {
//    e.preventDefault();
//    $(".overlay").show().css("overflow", "auto");
//    $("html").css("overflow-y", "hidden");
//    $(".content_form").animate({
//      top: "50%",
//    });
//  });
//  // Выплывающее окно
//  $(".overlay").click(function () {
//    $(".overlay").hide();
//    $("html").css("overflow-y", "scroll");
//    $(".content_form").animate({
//      top: "-150%",
//    });
//  });
//
//  $(".about__btn-modal-geo").click(function (e) {
//    e.preventDefault();
//    $(".overlay").show().css("overflow", "auto");
//    $("html").css("overflow-y", "hidden");
//    $(".geo-form").animate({
//      top: "50%",
//    });
//  });
//  // Выплывающее окно
//  $(".overlay").click(function () {
//    $(".overlay").hide();
//    $("html").css("overflow-y", "scroll");
//    $(".geo-form").animate({
//      top: "-150%",
//    });
//  });
//
//  // Форма вылета Social links
//  $(".header-info__btn").click(function (e) {
//    e.preventDefault();
//    $(".overlay").show().css("overflow", "auto");
//    $("html").css("overflow-y", "hidden");
//    $(".social-links-form").animate({
//      top: "50%",
//    });
//  });
//  // Выплывающее окно
//  $(".overlay").click(function () {
//    $(".overlay").hide();
//    $("html").css("overflow-y", "scroll");
//    $(".social-links-form").animate({
//      top: "-150%",
//    });
//  });
//
//  // Форма вылета DELETE BUTTON
//  $(".tabs-card__delete").click(function (e) {
//    e.preventDefault();
//    $(".overlay").show().css("overflow", "auto");
//    $("html").css("overflow-y", "hidden");
//    $(".delete-product").animate({
//      top: "50%",
//    });
//  });
//  // Выплывающее окно
//  $(".overlay").click(function () {
//    $(".overlay").hide();
//    $("html").css("overflow-y", "scroll");
//    $(".delete-product").animate({
//      top: "-100%",
//    });
//  });
//
//  // $(".product-form__video-link").click(function () {
//  //   $(".overlay").show().css("overflow", "auto");
//  //   $("html").css("overflow-y", "hidden");
//  //   $(".video-link").animate({
//  //     top: "50%",
//  //   });
//  // });
//  // // Выплывающее окно
//  // $(".overlay").click(function () {
//  //   $(".overlay").hide();
//  //   $("html").css("overflow-y", "scroll");
//  //   $(".video-link").animate({
//  //     top: "-150%",
//  //   });
//  // });
//  $(".online_shop_share").click(function () {
//    $(".overlay").show().css("overflow", "auto");
//    $("html").css("overflow-y", "hidden");
//    $(".online_shop_share_block_js").animate({
//      top: "50%",
//    });
//  });
//
//  $(".product_share").click(function () {
//    $(".overlay").show().css("overflow", "auto");
//    $("html").css("overflow-y", "hidden");
//    $(".product_share_block").animate({
//      top: "50%",
//    });
//  });
//  // Выплывающее окно
//  $(".overlay").click(function () {
//    $(".overlay").hide();
//    $("html").css("overflow-y", "scroll");
//    $(".online_shop_share_block_js").animate({
//      top: "-100%",
//    });
//  });
//
//  $(".overlay").click(function () {
//    $(".overlay").hide();
//    $("html").css("overflow-y", "scroll");
//    $(".product_share_block").animate({
//      top: "-100%",
//    });
//  });
//
//  $(".mobile-version__contact").click(function () {
//    $(".overlay").show().css("overflow", "auto");
//    $("html").css("overflow-y", "hidden");
//    $(".mobile-contacts-modal").animate({
//      bottom: "50%",
//    });
//  });
//  // Выплывающее окно
//  $(".overlay").click(function () {
//    $(".overlay").hide();
//    $("html").css("overflow-y", "scroll");
//    $(".mobile-contacts-modal").animate({
//      bottom: "-100%",
//    });
//  });


  // Файловый инпут

  $(".input_file input[type=file]").change(function () {
    var t = $(this).val();
    if (t.indexOf("C:\\fakepath\\") + 1) t = t.substr(12);
    var e = $(this).next().find(".fake_file_input");
    e.val(t);
  });

  // Мобильное меню
  const buttons = document.querySelectorAll(".menu__item");
  let activeButton = document.querySelector(".menu__item_active");

  buttons.forEach((item) => {
    const text = item.querySelector(".menu__text");
    setLineWidth(text, item);

    window.addEventListener("resize", () => {
      setLineWidth(text, item);
    });

    item.addEventListener("click", function () {
      if (this.classList.contains("menu__item_active")) return;

      this.classList.add("menu__item_active");

      handleTransition(this, text);
      activeButton = this;
    });
  });

  function setLineWidth(text, item) {
    const lineWidth = text.offsetWidth + "px";
    item.style.setProperty("--lineWidth", lineWidth);
  }

  function handleTransition(item, text) {
    item.addEventListener("transitionend", (e) => {
      if (
        e.propertyName != "flex-grow" ||
        !item.classList.contains("menu__item_active")
      )
        return;

      text.classList.add("menu__item_active");
    });
  }
});
