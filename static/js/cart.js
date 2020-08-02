var updateBtns =  document.getElementsByClassName('update-cart')
var removeFromCartbtn = document.getElementsByClassName('removeFromCart')
var addToCartbtn = document.getElementsByClassName('addToCart')
console.log(addToCartbtn)
console.log(removeFromCartbtn)
console.log(updateBtns)
for(i=0; i<addToCartbtn.length; i++){
	addToCartbtn[i].addEventListener('click',function(){
		// console.log(this.dataset.dish)
		addCookieItem(this.dataset.dish, 'addThroughCart', '', '')
	})
}
for(i=0; i<removeFromCartbtn.length; i++){
	removeFromCartbtn[i].addEventListener('click',function(){
		// console.log(this.dataset.dish)
		addCookieItem(this.dataset.dish, 'remove', '', '')
	})
}


for(i=0; i<updateBtns.length; i++){
	updateBtns[i].addEventListener('click', function(){
		var dishId = this.dataset.dish
		var action = this.dataset.action
		var dishComments = document.getElementById("comment_" +dishId )
		if(dishComments != null){
			dishComments =  dishComments.value
		}
		else{
			dishComments =  ''
		}
		var dishQuantity = document.getElementById('dishQuantity_'+dishId).value
		// console.log(dishQuantity)
		// print(dishQuantity)
		if(dishQuantity == 0){
			alert('Please enter the quantity');
        	// return false
		}
		else{
				addCookieItem(dishId, action, dishComments, dishQuantity)
				updateUserOrder(dishId, action, dishComments, dishQuantity)
				var x = document.getElementById("snackbar");
				  x.className = "show";
				  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
		}
		// console.log('dishId:', dishId, 'Action:', action, dishComments, dishQuantity)

		
	})
}

function addCookieItem(dishId, action, dishComments, dishQuantity){
	if(action == 'add'){
		
		cart[dishId]  = {
							'quantity':dishQuantity,
							'dishComments':dishComments,
						}
		
	}
	else if(action =='addThroughCart'){
		cart[dishId]['quantity'] = parseInt(cart[dishId]['quantity'])+1
		addToCartbtn =  null
		// location.reload()
	}
	else if(action == 'remove'){
		if(cart[dishId]['quantity'] == 1)
		{
			delete cart[dishId]
		}
		else{
			cart[dishId]['quantity'] -= 1
		}
		removeFromCartbtn =  null
		// location.reload()
	}
	
	document.cookie = 'cart='+ JSON.stringify(cart) +";domain=;path=/"
}

function updateUserOrder(dishId, action, dishComments, dishQuantity){

	var url = '/update_item/'

	fetch(url, {
		method: 'POST',
		headers:{
			'Content-Type': 'application/json',
			"X-CSRFToken":csrftoken,
		},
		body:JSON.stringify({
			'dishId':dishId,
			'action':action,
			'dishQuantity':dishQuantity,
			'dishComments': dishComments
		})
	})

		.then((response)=>{
			return response.json()
		})

		.then((data)=>{	
			console.log('data:', data)
			// location.reload()
		})

}

