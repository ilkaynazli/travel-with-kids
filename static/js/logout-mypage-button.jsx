function LogoutButton(props) {
    return (
        <button type='button' onClick={() => localStorage.removeItem('userId')}>
            <a href="/log-out">Log out</a>
        </button>
    );
}

function MyPageButton(props) {
    const userId = localStorage.getItem('userId');
    console.log('this is my page button: ', userId);
    // const userId = 3;
    return (
        <button type='button'>
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