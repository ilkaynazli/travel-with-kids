class LoginError extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
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
                    console.log(response);
                    console.log(response['question']);
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
                    Wrong username or password! <br/>
                    Please enter your email: 
                    <input type="text" name="email" value={this.state.email}
                                onChange={(event)=>this.handleChange(event)} /><br />
                    <input type="submit" value="Submit" />
                </form>
            ); 
        } 
    }
}

function SignupRoute(props) {
    return (
        <div>
            Please sign up <a href="/signup">here</a>.
        </div>
        );
}



