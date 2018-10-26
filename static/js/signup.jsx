class SignUp extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            questions: [],
            username: '',
            password: '',
            password2: '',
            email: '',
            userQuestion: '',
            answer: '',
            error: null,
            passwordHasError: false
        }
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.componentDidUpdate = this.componentDidUpdate.bind(this);
    }

    checkPassword() {
         if(this.state.password != this.state.password2) {
            this.setState({passwordHasError:true});
        }
        else {
            this.setState({passwordHasError:false});
        }
    }

    handleChange(evt) {
        const { name, value } = evt.target;

        this.setState({
                [name] : value 
            }, () => {
                if (name == 'password' || name == 'password2')
                    this.checkPassword();
                }
            );
    }

    componentDidMount(evt) {
        postData('/show-signup-button.json', this.state)
            .then((response) => {
                    console.log(response);
                    this.setState({questions: response['questions']});                
                })
            .catch((error) => console.error(error));
    }

    componentDidUpdate(prevState) {
        if (this.state.error == true) {
            this.setState({error: null});
        }
    }

    handleSubmit(evt) {
        evt.preventDefault();
        postData('/signup.json', this.state)
            .then((response) => {
                    console.log('this is signup handleSubmit ' + response);
                    this.setState({error: response['error']});                
                })
            .catch((error) => console.error(error));
    }

    render () {
        const questions = this.state.questions;
        const error = this.state.error;
        const passwordHasError = this.state.passwordHasError;
        if (error == false) {
            return (        
                    <div>
                        You have successfully signed up<br/>
                        <a href="/">Click here to go to homepage</a>
                    </div>
                );
        } else { 
            return (
                <div>
                    {error && alert("Password doesn't fit the requirements. Please try again!")}
                    {passwordHasError && 'The passwords do not match! Please try again!'}
                    <form onSubmit={this.handleSubmit}>
                        Username*: <input type="text" 
                                            name="username" 
                                            value={this.state.username}
                                            onChange={(event)=>this.handleChange(event)}/><br/>
                        Password*: <input type="password" 
                                            name="password" 
                                            value={this.state.password}
                                            onChange={(event)=>this.handleChange(event)}/><br/>
                        Please use at least one lowercase, one uppercase letter, one number, 
                        and one character (!@#$%^&*(){}[]/?)<br/>
                        Re-enter Password*: <input type="password" 
                                                    name="password2" 
                                                    value={this.state.password2}
                                                    onChange={(event)=>this.handleChange(event)}/><br/>
                        Email*: <input type="text" 
                                        name="email" 
                                        value={this.state.email}
                                        onChange={(event)=>this.handleChange(event)}/><br/>

                        <select name="userQuestion"                                 
                                value={this.state.userQuestion}
                                onChange={(event)=>this.handleChange(event)}>
                            {questions.map((question) => 
                                <option value={question['id']} 
                                        key={question['id']}>
                                            {question['question']}
                                        </option>)}
                        </select><br/>

                        Answer*: <input type="text" 
                                        name="answer" 
                                        value={this.state.answer}
                                        onChange={(event)=>this.handleChange(event)}/>
                        <input type="submit" value="Submit"/><br/><br/>
                        *These fields are required!
                    </form>
                </div>
        )}
    }
}

class SignUpButton extends React.Component {
    constructor(props) {
        super(props);
        this.state = {myClick: false};
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(evt) {
        evt.preventDefault();
        console.log('this is signUpButton: button pressed');
        this.setState({myClick: true});
    }

    render() { 
        const myClick = this.state.myClick;
        return (
            <div>
            {myClick ? <SignUp /> : <button type='button' 
                                            onClick={this.handleClick}>                
                                    Sign Up
                                </button>}           
            </div>
        ) 
    }
}


ReactDOM.render(
    <SignUpButton />, document.getElementById('signup')
);
