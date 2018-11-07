class LoginForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            userId: null,
            error: false,
            message: 'Wrong username or password!'
            }
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.doThisAfterClick = this.doThisAfterClick.bind(this);
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
                this.setState({userId: response['user_id'],
                                error: response['error']});
                localStorage.setItem('userId', response['user_id']);                                
            })
            .catch((error) => console.error(error));
    }

    doThisAfterClick(evt) {
        evt.preventDefault();
        this.setState({
            error: true,
            message: ''
        });
    }


    render() {
        const userId = this.state.userId;
        if (this.state.error == true) {
            return <LoginError message={this.state.message}/>
        } else if (userId != null) {
            return (
                <div>
                <MyPageButton userId={userId} />
                <LogoutButton />
                </div>
            );
        } else {
            return (
                    <div>
                    <form onSubmit={this.handleSubmit}>
                    <div className="form-group">
                        <label>Username:</label> 
                        <input type="text" 
                                className="form-control"
                                placeholder="Username"
                                name="username"
                                value={this.state.username}
                                onChange={(event) => this.handleChange(event)} /><br/>         
                        </div>
                        <div className="form-group">
                        <label>Password:</label>
                        <input type="password"
                                className="form-control"
                                placeholder="Password"
                                name="password"
                                value={this.state.password}
                                onChange={(event) => this.handleChange(event)} /><br/>
                        </div>
                        <input type="submit" 
                               value="Submit"
                               className="btn btn-info" /><br/>
                        Forgot password/username? 
                        <a href="#" onClick={(evt) => this.doThisAfterClick(evt)}>Click Here</a>
                    </form>
    </div>
            );
        }
    } 
}

function LogoutButton(props) {
    return (
        <button type='button' 
                className="btn btn-info"
                onClick={() => localStorage.removeItem('userId')}>
            <a href="/log-out">Log out</a>
        </button>
    );
}

function MyPageButton(props) {
    const userId = props.userId;
    console.log('this is in login button: ', userId);

    return (
        <button type='button'
                className="btn btn-info">
            <a href={"/users/"+userId}>My Page</a>
        </button>
    );
}

class LogInButton extends React.Component {
    constructor(props) {
        super(props);
        this.state = {myClick: false};
    }

    render() { 
        const myClick = this.state.myClick;
        return (
            <div>
            {myClick ? <LoginForm /> : <button type='button'
                                            className="btn btn-info" 
                                            onClick={(evt) => {evt.preventDefault();
                                                                this.setState({myClick: true})}}>                
                                Login 
                               </button>}           
            </div>
        ) 
    }
}

class MyUserButtons extends React.Component {
    constructor(props) {
        super(props);
        this.state = {isLoggedIn: false}
    }

    render () {
        return (
        <div className="btn-group">
            {!this.state.isLoggedIn && <SignUpButton />}
            <LogInButton />
        </div>
        )
    }
}

ReactDOM.render(
    <MyUserButtons />, document.getElementById('root')
);


