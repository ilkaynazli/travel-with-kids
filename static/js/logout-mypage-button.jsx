function LogoutButton(props) {
    return (
        <button type='button' 
                className="btn btn-info"
                onClick={() => localStorage.removeItem('userId')}>
            <a href="/log-out">Log out</a>
        </button>
    );
}

function MyPageButton(props) {
    const userId = localStorage.getItem('userId');
    return (
        <button type='button'
                className="btn btn-info">
            <a href={'/users/' + userId}>My page</a>
        </button>
    );
}

function MyLoggedInButtons(props) {
    return(
    <div>
        <MyPageButton />
        <LogoutButton />
    </div>
        )
}

ReactDOM.render(
    <MyLoggedInButtons />, document.getElementById('root')
    )