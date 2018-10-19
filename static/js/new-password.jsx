class NewPassword extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: props.username,
            password: '',
            password2: '',
            error: null,
            message: null,
            passwordHasError: false
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
        console.log(password);
        console.log(password2);
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
        const error = this.state.error;
        const message = this.state.message;
        const passwordHasError = this.state.passwordHasError;
        console.log('this is render:' + error + message + passwordHasError);

        if (error == false) {
            return (
                    <div>
                        {message}<br/>
                        <a href="/">Click here to go to homepage</a>
                    </div>
                );
        } else {
            return (
                <div>
                {passwordHasError && The passwords do not match! Please try again!<br/>}

                {error && {message}<br/>}

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
                </div>
            );
        }
    }
}


