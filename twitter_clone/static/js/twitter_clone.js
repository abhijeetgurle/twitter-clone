$(document).ready(function(){

	$("#followed_status").hover(function(){
        $(this).html("Unfollow");
        }, function(){
        $(this).html("Followed");
    });
});