$(document).on("click", ".usuarios", function () {
var id = $(this).data('id');
document.getElementById("link").setAttribute("href",'eliminar/'+id);
});
