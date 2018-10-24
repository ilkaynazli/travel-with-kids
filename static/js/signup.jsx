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
        // this.componentDidMount = this.componentDidMount.bind(this);
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


    handleSubmit(evt) {
        evt.preventDefault();
        postData('/signup.json', this.state)
            .then((response) => {
                    console.log(response);
                    this.setState({error: response['error']});                
                })
            .catch((error) => console.error(error));
    }

    render () {
        const questions = this.state.questions;
        return (
            <form onSubmit={this.handleSubmit}>
                Username*: <input type="text" 
                                    name="username" 
                                    value={this.state.username}/><br/>
                Password*: <input type="password" 
                                    name="password" 
                                    value={this.state.password}/><br/>
                Please use at least one lowercase, one uppercase letter, one number, 
                and one character (!@#$%^&*(){}[]/?)<br/>
                Re-enter Password*: <input type="password" 
                                            name="password2" 
                                            value={this.state.password2}/><br/>
                Email*: <input type="text" name="email" value={this.state.email}/><br/>

                <select name="userQuestion" value={this.state.value} onChange={this.handleChange}>
                    {this.componentDidMount()}
                    
                    questions.map(question=question.question, id=question['id']) => {<option value={id}>{question}</option>}
                    
                </select><br/>
                Answer*: <input type="text" name="answer" value={this.state.answer}/>
                <input type="submit" value="Submit"/><br/><br/>
                *These fields are required!
            </form>
        )
    }
}

function SignUpButton() {
    return (
        <button type='button'>
            <SignUp />
        </button>
    ) 
}

ReactDOM.render(
    <SignUpButton />, document.getElementById('signup')
);

//                     <option value='1'>What is your favorite color?</option>
//                     <option value='2'>What was the name of your first teacher?</option>
//                     <option value='3'>What was the model of your first car?</option>
//                     <option value='4'>What was your favorite toy as a child?</option>
//                     <option value='5'>Where is your favorite vacation destination?</option>
//                     <option value='6'>What was the name of your first pet?</option>
//             