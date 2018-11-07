class SignUp extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            questions: [],
            username: '',
            password: '',
            password2: '',
            email: '',
            userQuestion: 1,
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
                        You have successfully signed up
                    </div>
                );
        } else { 
            return (

                <div>
                    {error && alert("Password doesn't fit the requirements. Please try again!")}
                    {passwordHasError && 'The passwords do not match! Please try again!'}
                    <form onSubmit={this.handleSubmit}>
                        <div className="form-group"> 
                        <label>Username*: </label>
                                        <input type="text" 
                                            className="form-control"
                                            placeholder="Username"
                                            name="username" 
                                            value={this.state.username}
                                            onChange={(event)=>this.handleChange(event)}/><br/>
                        </div>
                        <div className="form-group"> 
                        <label>Password*: </label> 
                                        <input type="password" 
                                            className="form-control"
                                            placeholder="Password"
                                            name="password" 
                                            value={this.state.password}
                                            onChange={(event)=>this.handleChange(event)}/><br/>
                        Please use at least one lowercase, one uppercase letter, one number, 
                        and one character (!@#$%^&*(){}[]/?)<br/>
                        </div>
                        <div className="form-group"> 
                        <label>Re-enter Password*: </label>
                                            <input type="password" 
                                                    className="form-control"
                                                    placeholder="Password"
                                                    name="password2" 
                                                    value={this.state.password2}
                                                    onChange={(event)=>this.handleChange(event)}/><br/>
                        </div>
                        <div className="form-group"> 
                        <label>Email*: </label>
                                    <input type="email" 
                                        className="form-control"
                                        placeholder="Email"   
                                        name="email" 
                                        value={this.state.email}
                                        onChange={(event)=>this.handleChange(event)}/><br/>
                        </div>
                        <div className="form-group"> 
                        <label>Please select a question:</label>
                        <select multiple className="form-control"
                                name="userQuestion"                               
                                value={this.state.userQuestion}
                                onChange={(event)=>this.handleChange(event)}>
                            {questions.map((question) => 
                                <option value={question['id']} 
                                        key={question['id']}>
                                            {question['question']}
                                        </option>)}
                        </select><br/>
                        </div>
                        <div className="form-group"> 
                        <label>Answer*: </label>
                                    <input type="text" 
                                        className="form-control"
                                        placeholder="Answer"
                                        name="answer" 
                                        value={this.state.answer}
                                        onChange={(event)=>this.handleChange(event)}/>
                        </div>
                        <input type="submit" 
                               value="Submit"
                               className="btn btn-info" /><br/><br/>
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
        this.setState({myClick: true});
    }

    render() { 
        const myClick = this.state.myClick;
        return (
            <div>
            {myClick ? <SignUp /> : <button type='button' 
                                            className="btn btn-info"
                                            onClick={this.handleClick}>                
                                    Sign Up
                                </button>}           
            </div>
        ) 
    }
}
