class LoginForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            userId: '',
            error: ''
        }
        this.handleUserChange = this.handleUserChange.bind(this);
        this.handlePasswordChange = this.handlePasswordChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleUserChange(evt) {
        this.setState({
            username: evt.target.value    
        });
    }
    handlePasswordChange(evt) {
        this.setState({
            password: evt.target.value
        });
    }

    handleSubmit(evt) {
        evt.preventDefault();
        postData('/login.json', this.state)
            .then((data) => {
                this.setState({userId: data['user_id'],
                                error: data['error']});
            })
            .catch((error) => console.error(error));        
    }

    render() {
        if (this.state.error == true) {
            return <LoginError />
        } else if (this.state.userId != '') {
            const userId = this.state.userId;
            return (
                <div>
                <LogoutButton />
                <MyPageButton userId={userId} />
                </div>
            );
        } else {
            return (
                <form onSubmit={this.handleSubmit}>
                    Username: 
                    <input type="text" 
                            name="username"
                            value={this.state.username}
                            onChange={this.handleUserChange} /><br/>         
                    Password:
                    <input type="password"
                            name="password"
                            value={this.state.password}
                            onChange={this.handlePasswordChange} /><br/>
                    <input type="submit" value="Submit" /><br/>
                    Forgot password/username? <a href="/wrong-password">Click Here</a>
                </form>
            );
        }
    } 
}
function postData(url='', data={}) {
            console.log(data);
            console.log(JSON.stringify(data))
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
    return (
        <button type='button'>
            <a href="/log-out">Log out</a>
        </button>
    );
}

function MyPageButton(props) {
    const userId = props.userId;
    console.log(userId);
    return (
        <button type='button'>
            <a href={"/users/"+userId}>My page</a>
        </button>
    );
}

function SignupRoute(props) {
    return (
        <div>
            User does not exist. Please sign up <a href="/signup">here</a>.
        </div>
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
        this.handleEmailChange = this.handleEmailChange.bind(this);
    }

    handleEmailChange(evt) {
        this.setState({
            email: evt.target.value    
        });
        console.log(this.state.email);
    }

    handleSubmit(evt) {
        evt.preventDefault();
        postData('/forgot-password.json', this.state)
            .then((data) => {
                    console.log(data);
                    console.log(data['question'])
                })
            .catch((error) => console.error(error));;
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                Wrong username or password! <br/>
                Please enter your email: 
                <input type="text" name="email" value={this.state.email}
                            onChange={this.handleEmailChange} /><br />
                <input type="submit" value="Submit" />
            </form>
        );  
    }
}


ReactDOM.render(
    <LoginForm />, document.getElementById('root')
);