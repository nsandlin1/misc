(* Name: Novi Sandlin
 * Date: 1/7/2023
 * Course Number and Section: CSC 330 002
 * Quarter: Winter 2022/23
 * Project #: 1
 *)

fun parse(input_file) =
    let
        (* Create file instream *)
        val input_file_stream = TextIO.openIn(input_file)
       
        (* Return bool whether given char is demarkator option or none or else *)
        fun is_demarkative(SOME #" ") = true |
            is_demarkative(SOME #"=") = true |
            is_demarkative(SOME #"+") = true |
            is_demarkative(SOME #"-") = true |
            is_demarkative(SOME #"*") = true |
            is_demarkative(SOME #"/") = true |
            is_demarkative(NONE) = true |
            is_demarkative(l) = false

        (* collects until sees demarkator. bool is whether or not the next char is demarkator*)
        fun get_next_token_helper(curr_tok, true, ifile) =  curr_tok |
            get_next_token_helper(curr_tok, false, ifile) = get_next_token_helper(curr_tok^str(Option.valOf(TextIO.input1(ifile))), is_demarkative(TextIO.lookahead(ifile)), ifile)

        (* Collect next token. If next character is demarkator, it will be len 1. If not, variable len, must call helper to collect *)
        fun get_next_token(true, ifile) = str(Option.valOf(TextIO.input1(ifile))) |
            get_next_token(false, ifile) = get_next_token_helper("", is_demarkative(TextIO.lookahead(ifile)), ifile)

        (* Tokenize file contents *)
        fun tokenize(ifile) = if TextIO.lookahead(ifile)=NONE then nil else get_next_token(is_demarkative(TextIO.lookahead(ifile)), ifile)::tokenize(ifile)

        (* Returns whether a char list contains an invalid character *)
        fun valid_chars(nil) = true | valid_chars(l::ls) = (Char.isAlpha(l) orelse is_demarkative(SOME l)) andalso valid_chars(ls)

        (* Implement Restrictions on tokens: no integers anywhere *)
        fun valid_toks(nil) = true | valid_toks(l::ls) = valid_chars(explode(l)) andalso valid_toks(ls)

        (* Takes a list of tokenes and returns the token datatype array *)
        fun parser(nil) = nil | parser(" "::ls) = parser(ls) | parser("="::ls) = [EQ]@parser(ls) | parser("+"::ls) = [PL]@parser(ls) | parser("-"::ls) = [MI]@parser(ls) | parser("*"::ls) = [TI]@parser(ls) | parser("/"::ls) = [DI]@parser(ls) | parser(l::ls) = [ID l]@parser(ls)



        (* tokenized contents of file to remove redundency in gen_output *)
        val tokenized_contents = tokenize(input_file_stream)

        (* Generate function output *)
        fun gen_output(false) = (print("Compilation error\n"); []) | gen_output(true) = parser(tokenized_contents)

    in
        gen_output(valid_toks(tokenized_contents))
    end;
