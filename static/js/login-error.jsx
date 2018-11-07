class LoginError extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            message: props.message,
            email:'',
            question: ''
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        this.setState(
            {[event.target.name] : event.target.value }   
        );

    }

    handleSubmit(evt) {
        evt.preventDefault();
        postData('/forgot-password.json', this.state)
            .then((response) => {
                    this.setState({question: response['question']});                
                })
            .catch((error) => console.error(error));
    }

    render() {
        if (this.state.question != null && this.state.question != '') {
            return <ShowQuestion question={this.state.question}/>
        } else if (this.state.question == null) {
            return (
                <div>
                    User does not exist. <br/>
                    <SignupRoute />
                </div>
                );
        } else {
            return (
                <form onSubmit={this.handleSubmit}>
                    {this.state.message} <br/>
                    <div className="form-group">
                    <label>Please enter your email: </label>
                    <input type="email" 
                                name="email"
                                className="form-control"
                                placeholder="Email"
                                value={this.state.email}
                                onChange={(event)=>this.handleChange(event)} /><br />
                            </div>
                    <input type="submit" 
                           value="Submit"
                           className="btn btn-info" />
                </form>
            ); 
        } 
    }
}

function SignupRoute(props) {
    return (
        <div>
            Please sign up <a href="/signup.json">here</a>.
        </div>
        );
}



