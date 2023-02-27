window.addEventListener("load", function () {
  function Slider(sliderClass) {
    this.li = document.querySelectorAll(sliderClass + " .indicators li");
    this.images = document.querySelectorAll(sliderClass + " .slider__img");
    this.prev = document.querySelector(sliderClass + " .left");
    this.next = document.querySelector(sliderClass + " .right");
    this.ul = document.querySelector(sliderClass + " .indicators");
    this.counter = 0;
    let context = this;
    // let timer;
    // let array = [this.ul, this.next, this.prev];

    // for (var u = 0; u < array.length; u++) {
    //   array[u].onmouseover = function () {
    //     clearInterval(timer);
    //   };
    //   array[u].onmouseout = function () {
    //     autoplay();
    //   };
    // }
    for (var i = 0; i < this.li.length; i++) {
      this.li[i].addEventListener("click", function () {
        for (var j = 0; j < context.li.length; j++) {
          context.li[j].classList.remove("active-li");
          context.images[j].classList.remove("active");
        }
        this.classList.add("active-li");
        var slide = this.getAttribute("data-slide");
        context.images[slide].classList.add("active");
        context.counter = slide;
      });
    }
    this.prev.addEventListener("click", left);
    this.next.addEventListener("click", right);

    function left() {
      if (context.images[context.counter] !== undefined) {
        context.images[context.counter].classList.remove("active");
        context.li[context.counter].classList.remove("active-li");
        context.counter--;
        if (context.counter < 0) {
            context.counter = context.images.length - 1;
        }
        context.images[context.counter].classList.add("active");
        context.li[context.counter].classList.add("active-li");
        }
    }

    function right() {
      if (context.images[context.counter] !== undefined) {
        context.images[context.counter].classList.remove("active");
        context.li[context.counter].classList.remove("active-li");
        context.counter++;
        if (context.counter == context.images.length) {
            context.counter = 0;
        }
        context.images[context.counter].classList.add("active");
        context.li[context.counter].classList.add("active-li");
        }
//      else{
//        alert('Ты лунтик');
//      }
    }

    // function autoplay() {
    //   timer = setInterval(right, 2000);
    // }
    // autoplay();
  }

  new Slider(".slider");
//  new Slider(".slider_product_form");
});
