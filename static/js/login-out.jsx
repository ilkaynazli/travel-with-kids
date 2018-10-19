
class LoginForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            userId: null,
            error: false
        }
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState(
            {[event.target.name] : event.target.value }   
        );
    }
   
    handleSubmit(evt) {
        evt.preventDefault();
        postData('/login.json', this.state)
            .then((response) => {
                localStorage.setItem('cachedId', response['user_id']);
                this.setState({userId: response['user_id'],
                                error: response['error']});
            })
            .catch((error) => console.error(error));
    }

    render() {
        const cachedId = localStorage.getItem('cachedId');
        if (this.state.error == true) {
            return <LoginError />
        } else if (cachedId != null) {
            return (
                <div>
                <MyPageButton userId={cachedId} />
                <LogoutButton />
                </div>
            );
        } else {
            return (
                <form onSubmit={this.handleSubmit}>
                    Username: 
                    <input type="text" 
                            name="username"
                            value={this.state.username}
                            onChange={(event) => this.handleChange(event)} /><br/>         
                    Password:
                    <input type="password"
                            name="password"
                            value={this.state.password}
                            onChange={(event) => this.handleChange(event)} /><br/>
                    <input type="submit" value="Submit" /><br/>
                    Forgot password/username? <a href="/wrong-password">Click Here</a>
                </form>
            );
        }
    } 
}
function postData(url='', data={}) {
            return fetch(url, {
                method: 'POST',
                headers: {
                "Content-Type": "application/json; charset=utf-8",
                },
                body: JSON.stringify(data)               
            })
            .then((response) => response.json());
        }

function LogoutButton(props) {
    localStorage.removeItem('cachedId');
    return (
        <button type='button'>
            <a href="/log-out">Log out</a>
        </button>
    );
}

function MyPageButton(props) {
    const userId = props.userId;
    return (
        <button type='button'>
            <a href={"/users/"+userId}>My page</a>
        </button>
    );
}

class LoginError extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            email:'',
            question: ''
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        this.setState(
            {[event.target.name] : event.target.value }   
        );

    }

    handleSubmit(evt) {
        evt.preventDefault();
        postData('/forgot-password.json', this.state)
            .then((response) => {
                    console.log(response);
                    console.log(response['question']);
                    this.setState({question: response['question']});                
                })
            .catch((error) => console.error(error));
    }

    render() {
        if (this.state.question != null && this.state.question != '') {
            return <ShowQuestion question={this.state.question}/>
        } else if (this.state.question == null) {
            return (
                <div>
                    User does not exist. <br/>
                    <SignupRoute />
                </div>
                );
        } else {
            return (
                <form onSubmit={this.handleSubmit}>
                    Wrong username or password! <br/>
                    Please enter your email: 
                    <input type="text" name="email" value={this.state.email}
                                onChange={(event)=>this.handleChange(event)} /><br />
                    <input type="submit" value="Submit" />
                </form>
            ); 
        } 
    }
}

function SignupRoute(props) {
    return (
        <div>
            Please sign up <a href="/signup">here</a>.
        </div>
        );
}

class ShowQuestion extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            question: props.question,
            answer: '',
            username: null,
            error: ''
        }
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        this.setState(
            {[event.target.name] : event.target.value }   
        );
    }

    handleSubmit(evt) {
        evt.preventDefault();
        postData('/check-answer.json', this.state)
            .then((response) => {
                    console.log(response);
                    console.log(this.state.question);
                    console.log(response['error']);
                    this.setState({error: response['error'],
                                    username: response['username']});                
                })
            .catch((error) => console.error(error));
    }

    render() {
        if (this.state.error == false) {
            return <NewPassword username={this.state.username}/>
        } else  {
            return (
                if (this.state.error == true){
                    <div>
                        The answer does not match! Please try again:
                    </div>}

                <form onSubmit={this.handleSubmit}>
                    {this.state.question} <br/>
                    Please enter your answer here:
                    <input type="text" name="answer" value={this.state.answer}
                                onChange={(event)=>this.handleChange(event)} /><br />
                    <input type="submit" value="Submit" />
                </form>
            );
        }
    }
}

class NewPassword extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: props.username,
            password: '',
            password2: '',
            error: false,
            message: '',
            passwordHasError:false
        }
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    checkPassword() {
         if(!this.state.password || this.state.password != this.state.password2) {
            this.setState({passwordHasError:true});
        }
        else {
            this.setState({passwordHasError:false});
        }
    }

    handleChange(event) {
        const { name, value } = event.target

        this.setState({
                [name] : value 
            }, () => {
                if (name == 'password' || name == 'password2')
                    this.checkPassword();
                }
            );
    }

    handleSubmit(evt) {
        evt.preventDefault();
        postData('/new-password.json', this.state)
            .then((response) => {
                    console.log(response);
                    console.log(response['message']);
                    this.setState({message: response['message'],
                                    error: response['error']});                
                })
            .catch((error) => console.error(error));
    }

    render() {
        if (this.state.passwordHasError == true) {
            return(
                <div>
                    The passwords do not match! Please try again!
                    <NewPassword username={this.state.username}/>
                </div>
                );
        } else if (error == true) {
            const message = this.state.message; 
            return(
                <div>
                    {message}<br/>
                    <NewPassword username={this.state.username}/>
                </div>
                );
        } else {
            return (
                <form on Submit={this.handleSubmit}>
                    Password*: <input type="password" name="password" 
                                    value={this.state.password}
                                    onChange={(event)=>this.handleChange(event)}/><br/>
                    Please use at least one lowercase, one uppercase letter, one number, 
                    and one character (!@#$%^&*(){}[]/?)<br/>
                    Re-enter Password*: <input type="password" name="password2"  
                                    value={this.state.password2}
                                    onChange={(event)=>this.handleChange(event)}/><br/>
                    <input type="submit" value="Submit"/><br/><br/>
                    *These fields are required!
                </form>
            );
        }
    }
}


ReactDOM.render(
    <LoginForm />, document.getElementById('root')
);

