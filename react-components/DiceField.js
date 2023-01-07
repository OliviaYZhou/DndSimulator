import React, {Fragment} from 'react';
import {withRouter} from 'react-router-dom';
class DiceField extends React.Component {

    state = {
        diceList: [],
        diceValues: []
    }
    componentDidMount() {}
    afunction(){}

    render() {
        return (
            <div id='dice-field'>
                <div class='dice-platform'>
                    <span class='dice'>
                        <h3>Dice</h3>
                        <table>
                            <tbody>
                                {this.state.novelChapters.map((chapter) => {})}
                            </tbody>
                        </table>
                    </span>
                </div>

            </div>
        )
    }

}

export default withRouter(BookMainPage);