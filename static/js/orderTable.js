var tableNumber_btn =  document.getElementById('tableNumber_buttonid')
if(tableNumber_btn){
    tableNumber_btn.addEventListener('click',function(){
    var tableNumber = document.getElementById('table_number').value
    
    if (tableNumber.length < 1) {
        alert('Please enter the table number');
        return false
    }
    else{
        cart['table_number'] = tableNumber
        document.cookie = 'cart='+ JSON.stringify(cart) +";domain=;path=/"
        console.log(cart)
        document.getElementById("order_now_btn").style.visibility="visible";
    }
    
})

}
