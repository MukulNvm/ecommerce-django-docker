$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 4,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

// $('.plus-cart').click(function(){
//     var id= $(this).attr("pid").toString();
//     // current object
//     //  <span id="quantity" >{{cart.quantity}}</span>
//     // parenNode is div.my-3
//     var eml=this.parentNode.children[2]
//     $.ajax({
//         type:"Get",
//         url:"/pluscart",
//         data:{
//             prod_id:id
//         },
//         success:function(data){
//             eml.innerText=data.quantity 
//             document.getElementById("amount").innerText=data.amount 
//             document.getElementById("totalamount").innerText=data.totalamount 
//         }
//     }) 
// })

// $('.minus-cart').click(function(){
//     var id= $(this).attr("pid").toString();
//     // current object
//     //  <span id="quantity" >{{cart.quantity}}</span>
//     // parenNode is div.my-3
//     var eml=this.parentNode.children[2]
//     $.ajax({
//         type:"Get",
//         url:"/minuscart",
//         data:{
//             prod_id:id
//         },
//         success:function(data){
//             eml.innerText=data.quantity 
//             document.getElementById("amount").innerText=data.amount 
//             document.getElementById("totalamount").innerText=data.totalamount 
//         }
//     }) 
// })

// $('.remove-cart').click(function(){
//     var id= $(this).attr("pid").toString();
//     // current object
//     //  <span id="quantity" >{{cart.quantity}}</span>
//     // parenNode is div.my-3
//     var eml=this
//     $.ajax({
//         type:"Get",
//         url:"/removecart",
//         data:{
//             prod_id:id
//         },
//         success:function(data){
//             document.getElementById("amount").innerText=data.amount 
//             document.getElementById("totalamount").innerText=data.totalamount 
//             console.log(eml.parentNode.parentNode);
//             eml.parentNode.parentNode.parentNode.parentNode.remove() 
//         }
//     }) 
// })

function updateCartCount() {
    $.ajax({
        type: "GET",
        url: "/updatedcart/",
        success: function(data) {
            $("#cart-count").text(data.totalitems); // Update cart count dynamically
        }
    });
}

$('.plus-cart').click(function(){
    var id= $(this).attr("pid").toString();
    // current object
    //  <span id="quantity" >{{cart.quantity}}</span>
    // parenNode is div.my-3
    var eml=this.parentNode.children[2]
    $.ajax({
        type:"Get",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount 
            updateCartCount(); // Update cart count after removing an item
        }
    }) 
})

// Minus Cart Item
$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];

    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: { prod_id: id },
        success: function(data) {
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
            updateCartCount(); // Update cart count after removing an item
        }
    });
});

// Remove Cart Item
$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this;

    $.ajax({
        type: "GET",
        url: "/removecart",
        data: { prod_id: id },
        success: function(data) {
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
            eml.parentNode.parentNode.parentNode.parentNode.remove();
            updateCartCount(); // Update cart count after removing an item
        }
    });
});

// Call updateCartCount initially when the page loads
updateCartCount();
