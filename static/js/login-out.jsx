class LoginForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            userId: null,
            error: false,
            message: 'Wrong username or password!',
            isLoggedIn: props.isLoggedIn   
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
                console.log('this is login hs1: ', localStorage.getItem('userId'));
                this.setState({userId: response['user_id'],
                                error: response['error']});
                localStorage.setItem('userId', response['user_id']);                                
                console.log('this is login hs2: ', localStorage.getItem('userId'));
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

    componentDidUpdate() {
        if (this.state.isLoggedIn != localStorage.getItem('userId')) {
            this.setState({isLoggedIn: (localStorage.getItem('userId') ? true : false) });
        }
        console.log(this.state.isLoggedIn);
    }

    render() {
        const userId = this.state.userId;
        console.log('this is login r: ', userId);
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
        <button type='button' onClick={() => localStorage.removeItem('userId')}>
            <a href="/log-out">Log out</a>
        </button>
    );
}

function MyPageButton(props) {
    const userId = props.userId;
    console.log('this is in login button: ', userId);

    return (
        <button type='button'>
            <a href={"/users/"+userId}>My page</a>
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
            <div>
          {
           localStorage.getItem('userId')
            ? <LogOutButton />
            : ( <div>
                 <LogInButton />
                 <SignUpButton />
                 </div>
              )
          }
        </div>
        )
    }
}

ReactDOM.render(
    <MyUserButtons />, document.getElementById('root')
);


