class LoginForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password:'',
        }
        this.handleUserChange = this.handleUserChange.bind(this);
        this.handlePasswordChange = this.handlePasswordChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleUserChange(evt) {
        this.setState(
            username: evt.target.value    
        );
    }
    handlePasswordChange(evt) {
        this.setState(
            password: evt.target.value
        );
    }

    handleSubmit(evt) {
        alert('this worked');
        console.log(this.state.username);
        console.log(this.state.password);
        evt.preventDefault();
    }
    render() {
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
        )
    } 
}

ReactDOM.render(
    <LoginForm />, document.getElementById('root')
);