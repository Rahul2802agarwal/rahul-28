var updateBtns =  document.getElementsByClassName('update-cart')
var removeFromCartbtn = document.getElementsByClassName('removeFromCart')
for(i=0; i<removeFromCartbtn.length; i++){
	removeFromCartbtn[i].addEventListener('click',function(){
		console.log(this.dataset.dish)
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
		// console.log('dishId:', dishId, 'Action:', action, dishComments, dishQuantity)
		addCookieItem(dishId, action, dishComments, dishQuantity)
		updateUserOrder(dishId, action, dishComments, dishQuantity)
		
	})
}

function addCookieItem(dishId, action, dishComments, dishQuantity){
	if(action == 'add'){
		if(cart[dishId] == undefined){
			cart[dishId]  = {
								'quantity':dishQuantity,
								'dishComments':dishComments,
							}
		}
		else{
			console.log('add else')
			cart[dishId]['quantity'] +=1
		}
	}
	if(action == 'remove'){
		delete cart[dishId]

		location.reload()
	}
	console.log('Cart:', cart)
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
			location.reload()
		})

}