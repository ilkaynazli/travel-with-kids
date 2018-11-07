class ShowQuestion extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            question: props.question,
            answer: '',
            username: null,
            error: null
        }
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
        postData('/check-answer.json', this.state)
            .then((response) => {
                    this.setState({error: response['error'],
                                    username: response['username']});                
                })
            .catch((error) => console.error(error));
    }

    render() {
        const error = this.state.error;

        if (error == false) {
            return (
                <NewPassword username={this.state.username}/>
            );
        } else  {
            return (
                <div>
                {error && <div>The answer does not match! Please try again:</div>}
                <form onSubmit={this.handleSubmit}>
                    {this.state.question} <br/>
                    Please enter your answer here:
                    <input type="text" name="answer" value={this.state.answer}
                                onChange={(event)=>this.handleChange(event)} /><br />
                    <input type="submit" 
                           value="Submit"
                           className="btn btn-info" />
                </form>
            </div>
            );
        }
    }
}

