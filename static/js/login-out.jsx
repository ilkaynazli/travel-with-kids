class LoginForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password:'',
        }
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(evt) {
        const target = evt.target;
        let value;
        if (target.id === 'username') {
            value = target.username.value;
        } else {
            value = target.password.value;
        }
        const name = target.name;
        this.setState(
            [name]: value    
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
                        id="username"
                        value={this.state.username}
                        onChange={this.handleChange} /><br/>         
                Password:
                <input type="text"
                        name="password"
                        id="password" 
                        value={this.state.password}
                        onChange={this.handleChange} /><br/>
                <input type="submit" value="Login" /><br/>
                Forgot password/username? <a href="/wrong-password">Click Here</a>
            </form>
        )
    } 
}

ReactDOM.render(
    <LoginForm />, document.getElementById('root')
);