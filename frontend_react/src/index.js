import React from 'react';
import ReactDOM from 'react-dom';
import './css/top_bar.css';
import './css/message_style.css';
import './css/bootstrap.css';
import './css/bootstrap-dialog.css';



//Functional Components
function Topbar(props){
	var content = [];
	if(props.username){
		content.push(
			<li key={0} className='right'><a onClick={props.logoutHandler} id='logout'>Log out</a></li>
		);
		content.push(
			<li key={1} className='topbar'><a>{'Hello ' + props.username}</a></li>
		);
	}else{
		content.push(
			<li key={0} className='right'>
				<a onClick={()=>{document.getElementById('id02').style.display='block'}}>
					Register
				</a>
			</li>
		);
		content.push(
			<li key={1} className='right'>
				<a onClick={()=>{document.getElementById('id01').style.display='block'}}>
					Log in
				</a>
			</li>
		);

		content.push(
			<li key={2} className='topbar'><a>{'Hello Guest'}</a></li>
		);
	}
	return(
		<div className='top'> 
			<ul className='topbar'>
				{content}
			</ul>
		</div>
	);
}

function Botbar(props){
	var content = null;
	var message = 'sdfsdf';
	if(props.username){
		content = (
			<li className='bottombar'>
				<input onChange={env => {message=env.target}} className='bottombar'
				 placeholder='Type message here' id='message_input'/>
			</li>);
	}else{
			content=(<li className='bottombar'>
				<input disabled className='bottombar'
				 placeholder='Log in to send message' id='message_input'/>
			</li>);
	}
	return(
		<ul className='bottombar'>
			{content}
			<li className='right'>
				<a className='active' id='send' onClick={()=>{props.handleClick(message)}}>send</a>
			</li>
		</ul>
	);
}

function Message(props){
	var ts = new Date(props.item.create_date);
	return(
		<div className={props.index %2 === 0 ? 'container message' : 'container message darker'}>
			<p>{props.item.content}</p>
			<span className={props.index %2 === 0 ? 'time-left' : 'time-right'}>
				{props.item.username + " " + ts.toLocaleString()}
			</span>
		</div>
	);
}

function MessageBoard(props){

	var content = [];
	if(props.messageJSON.length > 0){
		content = props.messageJSON.map((item, index) => (
				<Message key={index} item={item} index={index}/>
		));	
	}
	return(			
		<div>
			{content} 
		</div>
	);
}


class LoginForm extends React.Component{
		constructor(props){
			super(props);
			this.state = {
				username: '',
				password: null,
			};

		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);

	}

	handleChange(event){
		this.setState({
			[event.target.name]: event.target.value,
		});

	}

	handleSubmit(){
		const uname = this.state.username;
		const pass = this.state.password;
		//showSuccessMessage(uname);
		if (uname === '' || pass === '') {
			showErrorMessage("Please fill all fields");		
		}else{
			
			window.$.ajax({
			  url: this.props.apiURL,
			  crossDomain: true,
			  type: "POST",
			  dataType:'json',
			  data: {username: uname,
					 password: pass},
			  statusCode: {
					403: () => {
						showErrorMessage("Password or Username is incorrect!");
					},
					
					200: (data) => {
						this.props.handleModal();
						this.props.loginCB(data);
						//var cookievalue = data.username + ":" + data.user_id;
						//setCookie('session', cookievalue, 1);
						//document.getElementById('id01').style.display='none';
						//location.reload();
					}
				},
			});
		}
	}

	render(){
		return(
      <div id="id01" className="modal">
        <form className="modal-content animate">
	      <div className="imgcontainer">
	        <span onClick={this.props.handleModal} className="close" title="Close Modal">&times;</span>
	        <p1 style={{'font-size':16+'pt', color:'grey'}}> Login </p1>
	      </div>
				<div className='form'>
	        <label><b>Username</b></label>
	        <input type="text" placeholder="Enter Username" 
	        	onChange={this.handleChange} name="username" required/>

	        <label><b>Password</b></label>
	        <input type="password" placeholder="Enter Password" 
	        	onChange={this.handleChange} name="password" required/>
	        <button type="button" style={{color:'white'}} className="confirmbtn" onClick={this.handleSubmit}>Login</button>
				</div>
				</form>
			</div>
		);
	}
}


class RegisterForm extends React.Component{
		constructor(props){
			super(props);
			this.state = {
				username: '',
				password: '',
				rpassword: '',
				email: '',
			};

		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);

	}

	handleChange(event){
		this.setState({
			[event.target.name]: event.target.value,
		});

	}

	handleSubmit(){
		const uname = this.state.username;
		const email = this.state.email;
		const pass = this.state.password;
		const rpass = this.state.rpassword;
		//showSuccessMessage(uname);
		if (uname === '' || pass === '' 
			  || rpass === '' || email === '') {
			showErrorMessage("Please fill all fields");		
		}else if (!validateEmail(email)){
			showErrorMessage("email format incorrect");
		}else if(pass.length < 8){
			showErrorMessage("Password should at least 8 character in length");
		}else if(!pass.match(rpass)){
			showErrorMessage("Your passwords don't match. Try again?");
		}else{
			
			window.$.ajax({
			  url: this.props.apiURL,
			  crossDomain: true,
			  type: "POST",
			  dataType:'json',
			  data: {username: uname,
			  			 email: email,
					 		 password: pass},
			  statusCode: {
					400: () => {
						showErrorMessage('Username is taken, please choose another one');

					},
					500: () => {
						showErrorMessage('Internal server error. Please try again later');
					},
					201: () => {
						showSuccessMessage('User created and you can now log in!');
						this.props.handleModal();
					}
				},
			});
		}
	}

	render(){
		return(
      <div id="id02" className="modal">
        <form className="modal-content animate">
	      <div className="imgcontainer">
	        <span onClick={this.props.handleModal} className="close" title="Close Modal">&times;</span>
	        <p1 style={{'font-size':16+'pt', color:'grey'}}> Register </p1>
	      </div>
				<div className='form'>
	        <label><b>Username</b></label>
	        <input type="text" placeholder="Enter Username" 
	        	onChange={this.handleChange} name="username" required/>
	        <label>Email :</label>
	        <input type="text" placeholder="Enter Email" 
	        	onChange={this.handleChange} name="email" required/>
	        <label><b>Password</b></label>
	        <input type="password" placeholder="Enter Password" 
	        	onChange={this.handleChange} name="password" required/>
	        <label>Confirm Password :</label>
	        <input type="password" placeholder="Retype Password" 
	        	onChange={this.handleChange} name="rpassword" required/>
	        <button type="button" style={{color:'white'}} className="confirmbtn" onClick={this.handleSubmit}>Register</button>
				</div>
				</form>
			</div>
		);
	}
}

class Wall extends React.Component{
	constructor(props){
		super(props);
		var session = sessionStorage.getItem('session');
		if(session)
			session = session.split(":");
		this.state = {
			username: session ? session[0] : null,
			user_id: session ? session[1] : null,
			messageJSON:[],
		};
		

		this.loginCallBack = this.loginCallBack.bind(this);
		this.logout = this.logout.bind(this);
		this.sendMsg = this.sendMsg.bind(this);
		this.fetchData = this.fetchData.bind(this);

	}

	componentDidMount(){
		this.fetchData();
		this.interval = setInterval(this.fetchData, 15*1000);
	}

	componentWillUnmount(){
		clearInterval(this.interval);
	}



	haha(){
		var c = this.refs.myInput.value;
		this.setState({content: c,}, ()=>{alert(this.state.content)});
	}

	loginCallBack(data){
		this.setState({
			username: data.username,
			user_id: data.user_id,
		});
		sessionStorage.setItem('session', data.username + ':'+data.user_id);
	}

	logout(){
		var value = sessionStorage.getItem("session").split(":");
		var name = value[0];
		var user_id = value[1];
		window.$.ajax({
		  url: "http://127.0.0.1:8000/api/users/logout/",
		  crossDomain: true,
		  type: "POST",
		  dataType:'json',
		  data: {username: name,
				 user_id: user_id},
		  success: (data) => {
				sessionStorage.removeItem('session');
				this.setState({
					user_id: null,
					username: null,
				});
				showSuccessMessage(name + " logged out!");
		  },
		});
	}

	sendMsg(inputElement){
		const uname = this.state.username;
		const user_id = this.state.user_id;
		var content = inputElement.value;
		
		
		if(user_id != null && content.trim() != ""){ // user logged in and input not empty
			window.$.ajax({
			  url: "http://127.0.0.1:8000/api/messages/",
			  crossDomain: true,
			  type: "POST",
			  dataType:'json',
			  data: {content: content,
					 username: uname,
					 user_id: user_id},
			  success: function(data){
					//refreshWall();
					//$("#message_input").val("");
					inputElement.value = '';
					this.fetchData();
			  }.bind(this),
			});

		}

	}

	fetchData(){
		window.$.ajax({
		  url: "http://127.0.0.1:8000/api/messages/",
		  type: "GET",
		  dataType:'json',
		  success: function(data){

				this.setState({
					messageJSON: data,
				});
		  }.bind(this),
		});
	}

	render(){

		const messages = this.state.messageJSON;

		return(
			<div>				
				<input ref='myInput' onChange={this.haha.bind(this)}/> 
				<LoginForm loginCB = {this.loginCallBack} apiURL='http://127.0.0.1:8000/api/users/login/' 
					handleModal={()=>{document.getElementById('id01').style.display='none'}}/>
				<RegisterForm  apiURL='http://127.0.0.1:8000/api/users/' 
					handleModal={()=>{document.getElementById('id02').style.display='none'}}/>
				<Topbar logoutHandler = {this.logout} username={this.state.username ? this.state.username : null}/>
				<MessageBoard  messageJSON = {messages}/>
				<Botbar handleClick={this.sendMsg} username={this.state.username ? this.state.username : null}/>
			</div>
		);
	}


}


ReactDOM.render(<Wall />, document.getElementById('root'));

/*
* Static Methods
*
*/
function validateEmail(email){  
	if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)){  
		return true;  
	}   
	return false;  
} 

function showErrorMessage(message){
	window.BootstrapDialog.show({
    type: window.BootstrapDialog.TYPE_DANGER,
    title: 'Error',
    message: message,
    buttons: [{
								label: 'Close',
								action: function(dialogItself){
									dialogItself.close();
								}
            	}]
  });
}

function showSuccessMessage(message){
	window.BootstrapDialog.show({
		type: window.BootstrapDialog.TYPE_SUCCESS,
		title: 'Success',
		message: message,
		buttons: [{
								label: 'Close',
								action: function(dialogItself){
									dialogItself.close();
								}
							}]
	});
}

