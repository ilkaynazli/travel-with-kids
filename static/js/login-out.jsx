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
                if (response['error'] == false) {
                    localStorage.setItem('cachedId', response['user_id']);
                }
                this.setState({userId: response['user_id'],
                                error: response['error']});
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
        const cachedId = localStorage.getItem('cachedId');
        if (this.state.error == true) {
            return <LoginError message={this.state.message}/>
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
                    Forgot password/username? 
                    <a href="#" onClick={(evt) => this.doThisAfterClick(evt)}>Click Here</a>
                </form>
            );
        }
    } 
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


ReactDOM.render(
    <LoginForm />, document.getElementById('root')
);

