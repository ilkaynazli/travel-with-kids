class LoginForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            userId: null,
            error: false
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
            .then((response) => {
                console.log('Userid is: ' + response['user_id']);
                console.log('All data received from server is: %O' , response);
                localStorage.setItem('cachedId', response['user_id']);
                this.setState({userId: response['user_id'],
                                error: response['error']});
            })
            .catch((error) => console.error(error));
    }

    render() {
        const cachedId = localStorage.getItem('cachedId');
        console.log('This is render. userID is: ' + cachedId);
        if (this.state.error == true) {
            return <LoginError />
        } else if (cachedId != null) {
            return (
                <div>
                <LogoutButton />
                <MyPageButton userId={cachedId} />
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
    localStorage.removeItem('cachedId');
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


ReactDOM.render(
    <LoginForm />, document.getElementById('root')
);


            // .then((question) => {
            //         console.log(question);
            //         if (question != '') {
            //             return <QuestionRoute question=question />
            //         } else {
            //             return <SignupRoute />
            //         }
            //     })