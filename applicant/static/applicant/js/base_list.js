window.addEventListener("scroll", function() {
  const head = document.querySelector(".head");
  const miniHead = document.querySelector(".mini_head");
  const content = document.querySelector(".content");
  const headHeight = head.offsetHeight; // Высота шапки

  if (window.scrollY > headHeight) {
    miniHead.classList.add("fixed");
    content.classList.add("content_after_fixed")
  } else {
    miniHead.classList.remove("fixed");
    content.classList.remove("content_after_fixed")
  }
});