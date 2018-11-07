class NewPassword extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: props.username,
            password: '',
            password2: '',
            error: null,
            passwordHasError: false
        }
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
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

    handleChange(event) {
        const { name, value } = event.target;

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
                    this.setState({error: response['error']});                
                })
            .catch((error) => console.error(error));
    }

    componentDidUpdate(prevState) {
        if (this.state.error == true) {
            this.setState({error: null});
        }
    }

    render() {
        const error = this.state.error;
        const passwordHasError = this.state.passwordHasError;
        if (error == false) {
            return (        
                    <div>
                        You have successfully changed your password!
                    </div>
                );
        } else {
            return (
                <div>
                {error && alert("Password doesn't fit the requirements. Please try again!")}
                {passwordHasError && 'The passwords do not match! Please try again!'}
                <br/>
                <form onSubmit={this.handleSubmit}>
                <div className="form-group">
                    <label>Password*: </label>
                                <input type="password" 
                                    name="password" 
                                    className="form-control"
                                    placeholder="Password"
                                    value={this.state.password} 
                                    onChange={(event)=>this.handleChange(event)}/><br/>
                    Please use at least one lowercase, one uppercase letter, one number, 
                    and one character (!@#$%^&*(){}[]/?)<br/>
                </div>
                <div className="form-group">
                    <label>Re-enter Password*: </label>
                            <input type="password" 
                                    name="password2"  
                                    className="form-control"
                                    placeholder="Password"
                                    value={this.state.password2}
                                    onChange={(event)=>this.handleChange(event)}/><br/>
                </div>
                    <input type="submit" 
                           value="Submit"
                           className="btn btn-info"/><br/><br/>
                    *These fields are required!
                </form>
                </div>
            );
        }
    }
}


