// Unhide elements in the form for add_ingredient.html
function unhideElements(ing_id){

    const form = "add_ing_form_" + ing_id 
    var add_ing_form = document.getElementById(form);

    // Unhide quantity label
    add_ing_form[0].previousElementSibling.hidden = false;

    // Unhide quantity dropdown
    add_ing_form[0].hidden = false;

    // Unhide unit label
    add_ing_form[1].previousElementSibling.hidden = false;

    // Unhide unit dropdown
    add_ing_form[1].hidden = false;

    // Hide + button
    add_ing_form[2].hidden = true;

    // Unhide "hide" button
    add_ing_form[3].hidden = false;

    // Show confirmation button
    add_ing_form[4].hidden = false;

}

// Hide elements in the form for add_ingredient.html
function hideElements(ing_id){

    const form = "add_ing_form_" + ing_id 
    var add_ing_form = document.getElementById(form);

    // Hide quantity label
    add_ing_form[0].previousElementSibling.hidden = true;

    // Hide quantity dropdown
    add_ing_form[0].hidden = true;

    // Hide unit label
    add_ing_form[1].previousElementSibling.hidden = true;

    // Hide unit dropdown
    add_ing_form[1].hidden = true;

    // Change button to show hide option of the options shown
    add_ing_form[2].hidden = false;

     // Unhide "hide" button
    add_ing_form[3].hidden = true;

    // Show confirmation button
    add_ing_form[4].hidden = true;
}