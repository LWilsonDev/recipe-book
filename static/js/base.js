$(document).ready(function() {
      //Materialize.css Jquery
      $('.collapsible').collapsible();
      $('select').material_select();
      $(".button-collapse").sideNav();
      $(".dropdown-button").dropdown();
      $('.modal').modal({
        dismissible: true,
        opacity: .5,
        inDuration: 300,
        outDuration: 200,
        startingTop: '4%',
        endingTop: '10%',
      });
      //Materialize JQuery END

      // Add recipe category validation
      $('.js_recipe_btn').click(function() {
        if (!$('.category_wrapper li').hasClass('selected'))
          alert("Please select a category for your recipe");
        if (!$('.vege_wrapper li').hasClass('selected'))
          alert("Please select an option to indicate if your recipe is suitable for vegetarians");
      });
      
     // pagination.js
     $('#myTable').pageMe({
    pagerSelector:'#myPager'});
});
